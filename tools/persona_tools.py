"""Persona management tools for Suno API."""

from core.client import client
from core.server import mcp
from core.utils import format_persona_result


@mcp.tool()
async def create_persona(
    audio_id: str,
    name: str,
) -> str:
    """Create a new artist persona from an existing audio.

    Save a voice style from a generated song to reuse in future generations.
    This allows you to maintain consistent vocals across multiple songs.

    Args:
        audio_id: ID of the audio to use as the persona reference
        name: Name for this persona (e.g., "My Rock Voice", "Soft Female Singer")
    """
    result = await client.create_persona(
        audio_id=audio_id,
        name=name,
    )
    return format_persona_result(result)
