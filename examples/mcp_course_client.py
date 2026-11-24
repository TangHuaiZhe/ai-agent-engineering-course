"""Independent stdio client that launches a real MCP SDK v2 server process.

Run from repository root:
    python3 -m examples.mcp_course_client
"""

from __future__ import annotations

import asyncio
import sys

from mcp import Client, StdioServerParameters


async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "examples.mcp_course_server"],
    )
    async with Client(params) as client:
        available = await client.list_tools()
        print("tools:", [tool.name for tool in available.tools])
        tasks = await client.call_tool("list_tasks", {})
        print("list_tasks:", tasks.structured_content or tasks.content)
        result = await client.call_tool("complete_task", {"task_id": "task-1"})
        print("complete_task (without approval):", result.structured_content or result.content)


if __name__ == "__main__":
    asyncio.run(main())
