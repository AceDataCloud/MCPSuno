"""Audio generation tools for Suno API."""

from core.client import client
from core.config import settings
from core.server import mcp
from core.utils import format_audio_result

DEFAULT_MODEL = settings.default_model


@mcp.tool()
async def generate_music(
    prompt: str,
    model: str = DEFAULT_MODEL,
    instrumental: bool = False,
) -> str:
    """Generate AI music from a text prompt (Inspiration Mode).

    This tool creates AI-generated music based on a simple text description.
    The AI will automatically generate appropriate lyrics, style, and melody.

    Args:
        prompt: Description of the music (e.g., "A happy birthday song", "Epic orchestral battle music")
        model: Model version. Options: chirp-v3, chirp-v3-5, chirp-v4, chirp-v4-5, chirp-v4-5-plus, chirp-v5
        instrumental: If True, generate music without vocals
    """
    result = await client.generate_audio(
        action="generate",
        prompt=prompt,
        model=model,
        instrumental=instrumental,
    )
    return format_audio_result(result)


@mcp.tool()
async def generate_custom_music(
    lyric: str,
    title: str,
    style: str = "",
    model: str = DEFAULT_MODEL,
    instrumental: bool = False,
    style_negative: str = "",
    vocal_gender: str = "",
) -> str:
    """Generate AI music with custom lyrics and style (Custom Mode).

    This tool gives you full control over the song's lyrics, title, and style.

    Args:
        lyric: Lyrics with section markers like [Verse], [Chorus], [Bridge]. Use newlines for line breaks.
        title: Title of the song
        style: Music style description (e.g., "pop rock, energetic", "acoustic, folk, gentle")
        model: Model version. Options: chirp-v3, chirp-v3-5, chirp-v4, chirp-v4-5, chirp-v4-5-plus, chirp-v5
        instrumental: If True, generate music without vocals
        style_negative: Styles to exclude (e.g., "heavy metal, screaming")
        vocal_gender: Voice gender: 'f' for female, 'm' for male (only for v4.5+ models)
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
async def extend_music(
    audio_id: str,
    lyric: str,
    continue_at: float,
    style: str = "",
    model: str = DEFAULT_MODEL,
) -> str:
    """Extend an existing song from a specific timestamp.

    Use this to continue a previously generated song with new lyrics.

    Args:
        audio_id: ID of the audio to extend (from a previous generation)
        lyric: Lyrics for the extended section with markers like [Verse], [Chorus]
        continue_at: Time in seconds where to continue (e.g., 120.5 = 2:00.5)
        style: Music style for the extension
        model: Model version to use
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
async def cover_music(
    audio_id: str,
    prompt: str = "",
    style: str = "",
    model: str = DEFAULT_MODEL,
) -> str:
    """Create a cover/remix version of an existing song.

    Generate a new version of a song with different style or arrangement.

    Args:
        audio_id: ID of the audio to cover
        prompt: Optional prompt describing the cover style
        style: Music style for the cover
        model: Model version to use
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
async def concat_music(audio_id: str) -> str:
    """Concatenate extended song segments into a complete song.

    After extending a song multiple times, use this to merge all segments
    into a single complete audio file.

    Args:
        audio_id: ID of the last segment of the extended song
    """
    result = await client.generate_audio(
        action="concat",
        audio_id=audio_id,
    )
    return format_audio_result(result)


@mcp.tool()
async def generate_with_persona(
    audio_id: str,
    persona_id: str,
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """Generate music using a saved artist persona/voice style.

    Use a previously created persona to maintain consistent vocal style
    across multiple songs.

    Args:
        audio_id: ID of the reference audio
        persona_id: ID of the persona (from create_persona tool)
        prompt: Description of the music to generate
        model: Model version to use
    """
    result = await client.generate_audio(
        action="artist_consistency",
        audio_id=audio_id,
        persona_id=persona_id,
        prompt=prompt,
        model=model,
    )
    return format_audio_result(result)
