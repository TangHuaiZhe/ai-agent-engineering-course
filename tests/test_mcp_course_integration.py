"""Optional MCP protocol integration tests. Run after installing mcp>=2,<3.

These tests communicate through the official MCP Client API in memory. They
are skipped when the optional SDK has not been installed.
"""

import importlib.util
import unittest

from examples.mcp_task_store import TaskStore

HAS_MCP = importlib.util.find_spec("mcp") is not None


@unittest.skipUnless(HAS_MCP, "Install requirements-mcp-lab.txt to run protocol tests")
class TestMCPV2Integration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        from examples.mcp_course_server import build_server

        self.store = TaskStore()
        self.server = build_server(self.store, actor="alice")

    async def test_tool_discovery(self):
        from mcp import Client

        async with Client(self.server) as client:
            result = await client.list_tools()
            names = {tool.name for tool in result.tools}
            self.assertIn("list_tasks", names)
            self.assertIn("complete_task", names)
            self.assertNotIn("approve_from_host", names)

    async def test_list_tasks_and_denied_completion(self):
        from mcp import Client

        async with Client(self.server) as client:
            tasks = await client.call_tool("list_tasks", {})
            self.assertFalse(tasks.is_error)
            self.assertIn("task-1", str(tasks.structured_content or tasks.content))
            self.assertNotIn("task-3", str(tasks.structured_content or tasks.content))
            attempt = await client.call_tool("complete_task", {"task_id": "task-1"})
            self.assertFalse(attempt.is_error)
            self.assertIn("approval_required", str(attempt.structured_content or attempt.content))
            self.assertEqual(self.store.tasks["task-1"]["status"], "open")

    async def test_host_approval_then_completion(self):
        from mcp import Client

        self.assertTrue(self.store.approve_from_host("alice", "task-1"))
        async with Client(self.server) as client:
            done = await client.call_tool("complete_task", {"task_id": "task-1"})
            self.assertFalse(done.is_error)
            self.assertIn("completed", str(done.structured_content or done.content))
            again = await client.call_tool("complete_task", {"task_id": "task-1"})
            self.assertIn("already_completed", str(again.structured_content or again.content))
            self.assertEqual(self.store.tasks["task-1"]["status"], "completed")

    async def test_cross_user_task_returns_not_found(self):
        from mcp import Client

        async with Client(self.server) as client:
            result = await client.call_tool("complete_task", {"task_id": "task-3"})
            self.assertFalse(result.is_error)
            self.assertIn("not_found", str(result.structured_content or result.content))
            self.assertEqual(self.store.tasks["task-3"]["status"], "open")


if __name__ == "__main__":
    unittest.main()
