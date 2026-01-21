"""Task query tools for Suno API."""


from core.client import client
from core.server import mcp
from core.utils import format_task_result


@mcp.tool()
async def get_task(task_id: str) -> str:
    """Query the status and result of a music generation task.

    Check if a generation is complete and get the resulting audio URLs.

    Args:
        task_id: The task ID returned from a generation request
    """
    result = await client.query_task(
        id=task_id,
        action="retrieve",
    )
    return format_task_result(result)


@mcp.tool()
async def get_tasks_batch(task_ids: list[str]) -> str:
    """Query multiple music generation tasks at once.

    Efficiently check the status of multiple tasks in a single request.

    Args:
        task_ids: List of task IDs to query
    """
    result = await client.query_task(
        ids=task_ids,
        action="retrieve_batch",
    )

    if "error" in result:
        error = result.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    lines = [f"Total Tasks: {result.get('count', 0)}", ""]

    for item in result.get("items", []):
        response_info = item.get("response", {})
        lines.extend(
            [
                f"=== Task: {item.get('id', 'N/A')} ===",
                f"Created At: {item.get('created_at', 'N/A')}",
                f"Success: {response_info.get('success', False)}",
            ]
        )

        for audio in response_info.get("data", []):
            lines.append(f"  - {audio.get('title', 'Untitled')}: {audio.get('audio_url', 'N/A')}")

        lines.append("")

    return "\n".join(lines)
