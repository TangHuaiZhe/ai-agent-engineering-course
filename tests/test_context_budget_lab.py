import unittest

from examples.context_budget_lab import Item, compare, evaluate, history, lexical_units, select_context


class TestContextBudgetLab(unittest.TestCase):
    def test_thirty_turns_and_same_gold_cases(self):
        events = history()
        self.assertEqual(len(events), 30)
        full, recent, summary = compare()
        self.assertEqual((full.retained, recent.retained, summary.retained), (5, 0, 5))
        self.assertFalse(full.budget_ok)
        self.assertTrue(recent.budget_ok)
        self.assertTrue(summary.budget_ok)
        self.assertLess(summary.units, recent.units)
        self.assertEqual((full.stale_facts, summary.stale_facts), (1, 0))

    def test_summary_preserves_latest_fact_constraints_todo_and_request(self):
        selected = select_context(history(), "summary_retrieval")
        values = {item.key: item.value for item in selected}
        self.assertEqual(values["risk"], "已修订")
        self.assertEqual(values["language"], "中文")
        self.assertEqual(values["unit"], "模拟单位")
        self.assertEqual(values["todo"], "核对风险来源")
        self.assertIn("引用来源", values["request"])
        self.assertNotIn("旧版本", [item.value for item in selected])

    def test_closed_todo_removed(self):
        events = history()
        events.append(Item("user", "todo_done", "todo", "已完成", "SIM-USER-31", 31))
        selected = select_context(events, "summary_retrieval")
        self.assertNotIn("todo", [item.key for item in selected])
        self.assertIn("todo", evaluate(selected, "summary_retrieval", 500).missing)

    def test_tool_instruction_attempt_remains_data(self):
        events = history()
        full = select_context(events, "full")
        summary = select_context(events, "summary_retrieval")
        attack = next(item for item in full if item.key == "instruction_attempt")
        self.assertEqual(attack.role, "tool")
        self.assertNotIn(attack, summary)
        self.assertTrue(evaluate(full, "full", 500).boundary_ok)
        self.assertTrue(evaluate(summary, "summary_retrieval", 500).boundary_ok)

    def test_forged_citation_source_not_counted(self):
        selected = select_context(history(), "summary_retrieval")
        forged = [
            Item(item.role, item.kind, item.key, item.value, "UNTRUSTED-WEB", item.turn)
            if item.key == "citation" else item
            for item in selected
        ]
        self.assertIn("citation", evaluate(forged, "summary_retrieval", 500).missing)

    def test_invalid_strategy_and_budget(self):
        with self.assertRaises(ValueError):
            select_context(history(), "unknown")
        with self.assertRaises(ValueError):
            evaluate([], "empty", 0)
        self.assertGreater(lexical_units("中文 API 123"), 0)


if __name__ == "__main__":
    unittest.main()
