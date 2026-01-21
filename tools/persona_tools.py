"""Persona management tools for Suno API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_persona_result


@mcp.tool()
async def suno_create_persona(
    audio_id: Annotated[
        str,
        Field(
            description="ID of the audio to use as the persona reference. This should be a previously generated song whose vocal style you want to save and reuse."
        ),
    ],
    name: Annotated[
        str,
        Field(
            description="Name for this persona. Use a descriptive name that helps you remember the voice style. Examples: 'My Rock Voice', 'Soft Female Singer', 'Deep Male Baritone', 'Energetic Pop Vocalist'"
        ),
    ],
) -> str:
    """Create a new artist persona from an existing audio's vocal style.

    This saves the vocal characteristics from a generated song so you can reuse
    that same voice style in future generations. Great for maintaining consistency
    across multiple songs.

    Use this when:
    - You generated a song and love the voice
    - You want to create multiple songs with the same vocalist
    - You're building an album with consistent vocal style
    - You want to save a unique voice for future use

    After creating a persona, use suno_generate_with_persona with the returned
    persona_id to generate new songs with that voice.

    Returns:
        Persona ID that can be used with suno_generate_with_persona tool.
    """
    result = await client.create_persona(
        audio_id=audio_id,
        name=name,
    )
    return format_persona_result(result)
