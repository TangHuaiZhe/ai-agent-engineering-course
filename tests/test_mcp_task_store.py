import unittest

from examples.mcp_task_store import TaskStore


class TestTaskStore(unittest.TestCase):
    def setUp(self):
        self.store = TaskStore()

    def test_alice_cannot_list_bob_task(self):
        visible = self.store.list_tasks("alice")
        self.assertEqual({task["id"] for task in visible}, {"task-1", "task-2"})

    def test_bob_only_sees_own_tasks(self):
        self.assertEqual([task["id"] for task in self.store.list_tasks("bob")], ["task-3"])

    def test_write_without_approval_is_denied(self):
        self.assertEqual(self.store.complete_task("alice", "task-1"), {"status": "approval_required"})
        self.assertEqual(self.store.tasks["task-1"]["status"], "open")

    def test_approval_and_completion(self):
        self.assertTrue(self.store.approve_from_host("alice", "task-1"))
        self.assertEqual(self.store.complete_task("alice", "task-1"), {"status": "completed"})
        self.assertEqual(self.store.tasks["task-1"]["status"], "completed")

    def test_repeat_completion_is_idempotent(self):
        self.store.approve_from_host("alice", "task-1")
        self.assertEqual(self.store.complete_task("alice", "task-1")["status"], "completed")
        self.assertEqual(self.store.complete_task("alice", "task-1")["status"], "already_completed")

    def test_cross_user_update_hides_existence(self):
        self.assertEqual(self.store.complete_task("alice", "task-3"), {"status": "not_found"})
        self.assertFalse(self.store.approve_from_host("alice", "task-3"))
        self.assertEqual(self.store.tasks["task-3"]["status"], "open")

    def test_approval_does_not_cover_other_task(self):
        self.store.approve_from_host("alice", "task-1")
        self.assertEqual(self.store.complete_task("alice", "task-2"), {"status": "approval_required"})

    def test_unknown_task(self):
        self.assertFalse(self.store.approve_from_host("alice", "none"))
        self.assertEqual(self.store.complete_task("alice", "none"), {"status": "not_found"})


if __name__ == "__main__":
    unittest.main()
