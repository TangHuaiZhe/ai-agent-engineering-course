"""Pure Python domain layer for Lab 02 (fictional data, no MCP dependency).

The host must originate an approval outside model-controlled tool arguments.
This is deliberately in-memory and NOT a production authorization service.
"""

from __future__ import annotations


class TaskStore:
    def __init__(self) -> None:
        self.tasks: dict[str, dict[str, str]] = {
            "task-1": {"owner": "alice", "title": "Read MCP specification", "status": "open"},
            "task-2": {"owner": "alice", "title": "Write tests", "status": "open"},
            "task-3": {"owner": "bob", "title": "Review another project", "status": "open"},
        }
        self.approvals: set[tuple[str, str]] = set()

    def list_tasks(self, actor: str) -> list[dict[str, str]]:
        """Return only tasks visible to the authenticated actor."""
        return [
            {"id": task_id, "title": task["title"], "status": task["status"]}
            for task_id, task in sorted(self.tasks.items())
            if task["owner"] == actor
        ]

    def approve_from_host(self, actor: str, task_id: str) -> bool:
        """Simulate approval from an authenticated host UI; never expose as a tool."""
        task = self.tasks.get(task_id)
        if task is None or task["owner"] != actor:
            return False
        self.approvals.add((actor, task_id))
        return True

    def complete_task(self, actor: str, task_id: str) -> dict[str, str]:
        task = self.tasks.get(task_id)
        if task is None or task["owner"] != actor:
            # Avoid revealing whether another user's task exists.
            return {"status": "not_found"}
        if (actor, task_id) not in self.approvals:
            return {"status": "approval_required"}
        if task["status"] == "completed":
            return {"status": "already_completed"}
        task["status"] = "completed"
        return {"status": "completed"}
