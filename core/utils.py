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
        "polling_interval_seconds": 15,
        "max_poll_attempts": 20,
        "expected_wait_seconds": 300,
        "next_step": (
            f'Call {poll_tool}(task_id="{task_id}") to poll until the task completes '
            f"and the final media URLs are available. "
            f"IMPORTANT: Media generation typically takes 1-5 minutes. "
            f"Wait at least 15 seconds between each poll. "
            f"Keep polling for up to 20 attempts. Do NOT stop early — the task is still running."
        ),
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
            "polling_interval_seconds": 15,
            "max_poll_attempts": 20,
            "next_step": (
                f'Task is NOT complete yet (state: "{state}"). '
                f'IMPORTANT: Only state="complete" with success=true means the task is finished. '
                f"Ignore any intermediate audio_url values — "
                f"these are streaming previews, NOT final results. "
                f'Wait 15 seconds, then call {poll_tool}(task_id="{task_id}") again. '
                f"Media generation typically takes 1-5 minutes. "
                f"Keep polling for up to 20 attempts. Do NOT stop early."
            ),
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
