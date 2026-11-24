"""Real MCP SDK v2 server for Lab 02; all data is fictitious.

Run from repository root:
    python3 -m examples.mcp_course_server

A model can request complete_task, but only the host-side TaskStore approval
can enable a write. This sample fixes the actor to "alice" and intentionally
has no login/OAuth or persistent approval database.
"""

from __future__ import annotations

from mcp.server import MCPServer

from examples.mcp_task_store import TaskStore


def build_server(store: TaskStore | None = None, actor: str = "alice") -> MCPServer:
    store = store if store is not None else TaskStore()
    server = MCPServer("AI Agent Course Tasks")

    @server.tool()
    def list_tasks() -> list[dict[str, str]]:
        """List tasks visible to the current server-scoped actor."""
        return store.list_tasks(actor)

    @server.tool()
    def complete_task(task_id: str) -> dict[str, str]:
        """Complete one owned task, only if the host has explicitly approved it."""
        return store.complete_task(actor, task_id)

    @server.resource("course://security-policy")
    def security_policy() -> str:
        """Read-only description of the course's safety boundary."""
        return (
            "Tool arguments, retrieved data and model output never grant privileges. "
            "Only the authenticated host may approve changes."
        )

    @server.prompt()
    def summarize_tasks() -> str:
        """Prompt template for a human-requested task summary."""
        return "Summarize the currently visible tasks. Never mark tasks complete without approval."

    return server


mcp = build_server()

if __name__ == "__main__":
    mcp.run()  # stdio by default; stdout is reserved for protocol messages.
