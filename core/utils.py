"""Utility functions for MCP Suno server."""

from typing import Any


def format_audio_result(data: dict[str, Any]) -> str:
    """Format audio generation result for display.

    Args:
        data: API response dictionary

    Returns:
        Formatted string representation of the result
    """
    if not data.get("success", False):
        error = data.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    lines = [
        f"Task ID: {data.get('task_id', 'N/A')}",
        f"Trace ID: {data.get('trace_id', 'N/A')}",
        "",
    ]

    audios = data.get("data", [])
    for i, audio in enumerate(audios, 1):
        lines.extend(
            [
                f"--- Song {i} ---",
                f"ID: {audio.get('id', 'N/A')}",
                f"Title: {audio.get('title', 'N/A')}",
                f"Style: {audio.get('style', 'N/A')}",
                f"Duration: {audio.get('duration', 0):.2f}s",
                f"State: {audio.get('state', 'N/A')}",
                f"Model: {audio.get('model', 'N/A')}",
                f"Audio URL: {audio.get('audio_url', 'N/A')}",
                f"Video URL: {audio.get('video_url') or 'N/A'}",
                f"Image URL: {audio.get('image_url', 'N/A')}",
                "",
                "Lyrics:",
                audio.get("lyric") or "N/A",
                "",
            ]
        )

    return "\n".join(lines)


def format_lyrics_result(data: dict[str, Any]) -> str:
    """Format lyrics generation result for display.

    Args:
        data: API response dictionary

    Returns:
        Formatted string representation of the result
    """
    if not data.get("success", False):
        error = data.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    lyrics_data = data.get("data", {})

    # Handle both list and dict response formats
    if isinstance(lyrics_data, list):
        # API returns a list of lyrics options
        lines = [f"Task ID: {data.get('task_id', 'N/A')}", ""]
        for i, item in enumerate(lyrics_data, 1):
            lines.extend(
                [
                    f"--- Option {i} ---",
                    f"Title: {item.get('title', 'N/A')}",
                    f"Status: {item.get('status', 'N/A')}",
                    "",
                    "Lyrics:",
                    item.get("text", "N/A"),
                    "",
                ]
            )
        return "\n".join(lines)
    else:
        # Single lyrics response
        return f"""Task ID: {data.get("task_id", "N/A")}
Title: {lyrics_data.get("title", "N/A")}
Status: {lyrics_data.get("status", "N/A")}

Lyrics:
{lyrics_data.get("text", "N/A")}
"""


def format_task_result(data: dict[str, Any]) -> str:
    """Format task query result for display.

    Args:
        data: API response dictionary

    Returns:
        Formatted string representation of the result
    """
    if "error" in data:
        error = data.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    request_info = data.get("request", {})
    response_info = data.get("response", {})

    lines = [
        f"Task ID: {data.get('id', 'N/A')}",
        f"Created At: {data.get('created_at', 'N/A')}",
        "",
        "Request:",
        f"  Action: {request_info.get('action', 'N/A')}",
        f"  Prompt: {request_info.get('prompt', 'N/A')}",
        "",
    ]

    if response_info.get("success"):
        lines.append("Response: Success")
        lines.append("")

        for i, audio in enumerate(response_info.get("data", []), 1):
            lines.extend(
                [
                    f"--- Song {i} ---",
                    f"ID: {audio.get('id', 'N/A')}",
                    f"Title: {audio.get('title', 'N/A')}",
                    f"Duration: {audio.get('duration', 0):.2f}s",
                    f"Audio URL: {audio.get('audio_url', 'N/A')}",
                    "",
                ]
            )
    else:
        lines.append(f"Response: {response_info}")

    return "\n".join(lines)


def format_persona_result(data: dict[str, Any]) -> str:
    """Format persona creation result for display.

    Args:
        data: API response dictionary

    Returns:
        Formatted string representation of the result
    """
    if not data.get("success", False):
        error = data.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    persona_data = data.get("data", {})
    return f"""Persona Created Successfully!
Task ID: {data.get("task_id", "N/A")}
Persona ID: {persona_data.get("persona_id", "N/A")}

You can use this persona_id with the generate_with_persona tool.
"""
