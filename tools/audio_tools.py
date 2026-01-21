"""Audio generation tools for Suno API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, SunoModel, VocalGender
from core.utils import format_audio_result


@mcp.tool()
async def suno_generate_music(
    prompt: Annotated[
        str,
        Field(
            description="Description of the music to generate. Be descriptive about genre, mood, instruments, and theme. Examples: 'A happy birthday song with acoustic guitar', 'Epic orchestral battle music with dramatic choir', 'Chill lo-fi hip hop beat for studying'"
        ),
    ],
    model: Annotated[
        SunoModel,
        Field(
            description="Suno model version. 'chirp-v4-5' is recommended for most use cases. 'chirp-v5' offers best quality with 8-minute max duration. Older models (v3, v3-5, v4) have shorter duration limits."
        ),
    ] = DEFAULT_MODEL,
    instrumental: Annotated[
        bool,
        Field(
            description="If true, generate instrumental music without vocals. Default is false (with vocals)."
        ),
    ] = False,
) -> str:
    """Generate AI music from a text prompt using Suno's Inspiration Mode.

    This is the simplest way to create music - just describe what you want and Suno
    will automatically generate appropriate lyrics, melody, style, and arrangement.

    Use this when:
    - You want quick music generation with minimal input
    - You don't have specific lyrics in mind
    - You want Suno to be creative with the arrangement

    For full control over lyrics and style, use suno_generate_custom_music instead.

    Returns:
        Task ID and generated audio information including URLs, title, lyrics, and duration.
    """
    result = await client.generate_audio(
        action="generate",
        prompt=prompt,
        model=model,
        instrumental=instrumental,
    )
    return format_audio_result(result)


@mcp.tool()
async def suno_generate_custom_music(
    lyric: Annotated[
        str,
        Field(
            description="Song lyrics with section markers. Use [Verse], [Chorus], [Pre-Chorus], [Bridge], [Outro], [Intro] to structure the song. Example:\n[Verse 1]\nWalking down the empty street\nRain is falling at my feet\n\n[Chorus]\nBut I keep moving on\nUntil the break of dawn"
        ),
    ],
    title: Annotated[
        str,
        Field(description="Title of the song. Keep it concise and memorable."),
    ],
    style: Annotated[
        str,
        Field(
            description="Music style description. Be specific about genre, mood, tempo, and instruments. Examples: 'upbeat pop rock, energetic drums, electric guitar', 'acoustic folk, gentle, fingerpicking', 'dark electronic, synthwave, 80s retro'"
        ),
    ] = "",
    model: Annotated[
        SunoModel,
        Field(
            description="Suno model version. 'chirp-v4-5' or 'chirp-v5' recommended for best quality."
        ),
    ] = DEFAULT_MODEL,
    instrumental: Annotated[
        bool,
        Field(
            description="If true, generate instrumental version (lyrics will be ignored). Default is false."
        ),
    ] = False,
    style_negative: Annotated[
        str,
        Field(
            description="Styles to explicitly exclude from the generation. Examples: 'heavy metal, screaming', 'autotune, electronic'"
        ),
    ] = "",
    vocal_gender: Annotated[
        VocalGender,
        Field(
            description="Preferred vocal gender. 'f' for female, 'm' for male, empty string for AI to decide. Only works with v4.5+ models."
        ),
    ] = "",
) -> str:
    """Generate AI music with full control over lyrics, title, and style (Custom Mode).

    This gives you complete creative control over the song. You provide the lyrics
    with section markers, and Suno generates the melody and arrangement.

    Use this when:
    - You have specific lyrics you want to use
    - You want precise control over the music style
    - You need a specific song title
    - You want to specify vocal gender (v4.5+ models)

    For quick generation without writing lyrics, use suno_generate_music instead.

    Returns:
        Task ID and generated audio information including URLs, title, lyrics, and duration.
    """
    payload = {
        "action": "generate",
        "custom": True,
        "lyric": lyric,
        "title": title,
        "model": model,
        "instrumental": instrumental,
    }

    if style:
        payload["style"] = style
    if style_negative:
        payload["style_negative"] = style_negative
    if vocal_gender and vocal_gender in ("f", "m"):
        payload["vocal_gender"] = vocal_gender

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def suno_extend_music(
    audio_id: Annotated[
        str,
        Field(
            description="ID of the audio to extend. This is the 'id' field from a previous generation result."
        ),
    ],
    lyric: Annotated[
        str,
        Field(
            description="Lyrics for the extended section. Use section markers like [Verse], [Chorus], [Bridge], [Outro]. The extension will continue from where the original song left off."
        ),
    ],
    continue_at: Annotated[
        float,
        Field(
            description="Timestamp in seconds where to start the extension. For example, 120.5 means continue from 2 minutes and 0.5 seconds into the song."
        ),
    ],
    style: Annotated[
        str,
        Field(
            description="Music style for the extension. Leave empty to maintain the original style, or specify to change the style mid-song."
        ),
    ] = "",
    model: Annotated[
        SunoModel,
        Field(description="Model version to use for the extension."),
    ] = DEFAULT_MODEL,
) -> str:
    """Extend an existing song from a specific timestamp with new lyrics.

    This allows you to continue a previously generated song, adding new sections
    like additional verses, a bridge, or an outro.

    Use this when:
    - A generated song is too short and you want to add more
    - You want to add a bridge or outro to an existing song
    - You're building a longer song piece by piece

    After extending multiple times, use suno_concat_music to merge all segments.

    Returns:
        Task ID and the extended audio information.
    """
    payload = {
        "action": "extend",
        "audio_id": audio_id,
        "lyric": lyric,
        "continue_at": continue_at,
        "custom": True,
        "model": model,
    }

    if style:
        payload["style"] = style

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def suno_cover_music(
    audio_id: Annotated[
        str,
        Field(
            description="ID of the audio to create a cover of. This is the 'id' field from a previous generation."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of how you want the cover to sound. Examples: 'acoustic unplugged version', 'jazz lounge style', '80s synthwave remix'"
        ),
    ] = "",
    style: Annotated[
        str,
        Field(
            description="Target music style for the cover. Examples: 'jazz, smooth, saxophone', 'acoustic folk, gentle guitar', 'electronic dance, high energy'"
        ),
    ] = "",
    model: Annotated[
        SunoModel,
        Field(description="Model version to use for the cover."),
    ] = DEFAULT_MODEL,
) -> str:
    """Create a cover or remix version of an existing song in a different style.

    This generates a new version of a song with a different arrangement, genre,
    or mood while keeping the core melody and lyrics.

    Use this when:
    - You want to hear a song in a different genre
    - You want an acoustic/unplugged version of an electronic song
    - You want to remix a song with a different vibe

    Returns:
        Task ID and the cover audio information.
    """
    payload = {
        "action": "cover",
        "audio_id": audio_id,
        "model": model,
    }

    if prompt:
        payload["prompt"] = prompt
    if style:
        payload["style"] = style

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def suno_concat_music(
    audio_id: Annotated[
        str,
        Field(
            description="ID of the LAST segment of an extended song chain. Suno will automatically find and merge all connected segments."
        ),
    ],
) -> str:
    """Concatenate extended song segments into a single complete audio file.

    After extending a song multiple times with suno_extend_music, use this tool
    to merge all the segments into one continuous audio file.

    Use this when:
    - You've extended a song one or more times
    - You want a single audio file instead of multiple segments
    - You're ready to finalize a long-form composition

    Returns:
        Task ID and the concatenated audio information with the full song.
    """
    result = await client.generate_audio(
        action="concat",
        audio_id=audio_id,
    )
    return format_audio_result(result)


@mcp.tool()
async def suno_generate_with_persona(
    audio_id: Annotated[
        str,
        Field(description="ID of a reference audio to base the generation on."),
    ],
    persona_id: Annotated[
        str,
        Field(
            description="ID of the persona to use. Get this from suno_create_persona tool. The persona defines the vocal style and characteristics."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of the music to generate. The persona's voice will be applied to this new song."
        ),
    ],
    model: Annotated[
        SunoModel,
        Field(description="Model version to use."),
    ] = DEFAULT_MODEL,
) -> str:
    """Generate music using a saved artist persona for consistent vocal style.

    This allows you to maintain a consistent voice/singing style across multiple
    songs by using a previously saved persona.

    Use this when:
    - You want multiple songs with the same vocal style
    - You're creating an album or series with consistent vocals
    - You found a voice you like and want to reuse it

    First create a persona with suno_create_persona, then use its ID here.

    Returns:
        Task ID and generated audio information with the persona's voice applied.
    """
    result = await client.generate_audio(
        action="artist_consistency",
        audio_id=audio_id,
        persona_id=persona_id,
        prompt=prompt,
        model=model,
    )
    return format_audio_result(result)
