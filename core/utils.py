"""Utility functions for MCP Suno server."""

import json
from typing import Any


def _with_submission_guidance(
    data: dict[str, Any], poll_tool: str, batch_poll_tool: str | None = None
) -> dict[str, Any]:
    """Attach MCP polling guidance to async submission responses."""
    payload = dict(data)
    task_id = payload.get("task_id")
    if not task_id:
        return payload

    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": poll_tool,
        "batch_poll_tool": batch_poll_tool,
        "next_step": f'Call {poll_tool}(task_id="{task_id}") to poll until the task completes and the final media URLs are available.',
    }
    return payload


def _with_task_guidance(
    data: dict[str, Any], poll_tool: str, batch_poll_tool: str | None = None
) -> dict[str, Any]:
    """Attach MCP polling guidance to task lookup responses."""
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
    if not task_id:
        return payload

    # Determine task state for explicit guidance
    state = payload.get("state", "")
    response = payload.get("response", {})
    success = response.get("success", False) if isinstance(response, dict) else False

    if state == "complete" and success:
        payload["mcp_task_polling"] = {
            "task_id": task_id,
            "state": state,
            "is_complete": True,
            "note": "Task is complete. The audio URLs are final and ready to present to the user.",
        }
    else:
        payload["mcp_task_polling"] = {
            "task_id": task_id,
            "poll_tool": poll_tool,
            "batch_poll_tool": batch_poll_tool,
            "state": state,
            "is_complete": False,
            "next_step": f'Task is NOT complete yet (state: "{state}"). '
            f'IMPORTANT: Only state="complete" with success=true means the task is finished. '
            f"Ignore any intermediate audio_url values (e.g. audiopipe.suno.ai URLs) — "
            f"these are streaming previews, NOT final results. "
            f'Call {poll_tool}(task_id="{task_id}") again after a few seconds.',
        }
    return payload


def format_audio_result(data: dict[str, Any]) -> str:
    """Format audio generation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "suno_get_task", "suno_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_lyrics_result(data: dict[str, Any]) -> str:
    """Format lyrics generation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "suno_get_task", "suno_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_task_result(data: dict[str, Any]) -> str:
    """Format task query result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_task_guidance(data, "suno_get_task", "suno_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_persona_result(data: dict[str, Any]) -> str:
    """Format persona creation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "suno_get_task", "suno_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )
