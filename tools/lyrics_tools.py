"""Lyrics generation tools for Suno API."""

from core.client import client
from core.server import mcp
from core.utils import format_lyrics_result


@mcp.tool()
async def generate_lyrics(
    prompt: str,
    model: str = "chirp-v3",
) -> str:
    """Generate song lyrics from a text prompt.

    Create structured lyrics with verse, chorus, and bridge sections
    based on your description.

    Args:
        prompt: Description of the lyrics you want (e.g., "A romantic ballad about lost love")
        model: Model version (default: chirp-v3)
    """
    result = await client.generate_lyrics(
        prompt=prompt,
        model=model,
    )
    return format_lyrics_result(result)
