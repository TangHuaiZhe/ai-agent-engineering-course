import unittest

from examples.versioned_memory import MemoryPolicyError, VersionedMemory


class TestVersionedMemory(unittest.TestCase):
    def setUp(self):
        self.memory = VersionedMemory()

    def test_first_write_is_version_one(self):
        r = self.memory.set("language", "zh", source="explicit_user_statement")
        self.assertEqual((r.version, r.status, r.supersedes), (1, "active", None))

    def test_update_supersedes_previous(self):
        first = self.memory.set("editor", "Vim", source="explicit_user_statement")
        second = self.memory.set("editor", "VS Code", source="explicit_user_statement")
        self.assertEqual(first.status, "superseded")
        self.assertEqual(second.version, 2)
        self.assertEqual(second.supersedes, first.record_id)
        self.assertEqual(self.memory.current("editor").value, "VS Code")

    def test_history_preserves_versions(self):
        self.memory.set("editor", "Vim", source="explicit_user_statement")
        self.memory.set("editor", "VS Code", source="explicit_user_statement")
        history = self.memory.history("editor")
        self.assertEqual([r.version for r in history], [1, 2])
        self.assertEqual([r.status for r in history], ["superseded", "active"])

    def test_delete_removes_current_view(self):
        self.memory.set("editor", "VS Code", source="explicit_user_statement")
        self.assertTrue(self.memory.delete("editor"))
        self.assertIsNone(self.memory.current("editor"))
        self.assertEqual(self.memory.history("editor")[-1].status, "deleted")

    def test_rewrite_after_delete_continues_version_history(self):
        first = self.memory.set("editor", "Vim", source="explicit_user_statement")
        self.memory.delete("editor")
        second = self.memory.set("editor", "VS Code", source="explicit_user_statement")
        self.assertEqual(second.version, 2)
        self.assertEqual(second.supersedes, first.record_id)
        self.assertEqual(self.memory.current("editor").value, "VS Code")

    def test_delete_missing_is_false(self):
        self.assertFalse(self.memory.delete("missing"))

    def test_external_web_content_cannot_write_memory(self):
        with self.assertRaises(MemoryPolicyError):
            self.memory.set("favorite_color", "red", source="web_page")

    def test_model_inference_cannot_write_memory(self):
        with self.assertRaises(MemoryPolicyError):
            self.memory.set("risk_profile", "aggressive", source="model_inference")

    def test_verified_project_fact_allowed(self):
        r = self.memory.set("project_branch", "main", source="verified_project_fact")
        self.assertEqual(r.value, "main")

    def test_blank_key_rejected(self):
        with self.assertRaises(MemoryPolicyError):
            self.memory.set("  ", "x", source="explicit_user_statement")

    def test_separate_keys_keep_separate_active_records(self):
        self.memory.set("a", 1, source="explicit_user_statement")
        self.memory.set("b", 2, source="explicit_user_statement")
        self.assertEqual(self.memory.current("a").value, 1)
        self.assertEqual(self.memory.current("b").value, 2)


if __name__ == "__main__":
    unittest.main()
