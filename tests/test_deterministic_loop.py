import unittest

from examples.deterministic_loop import Action, SimulatedPlanner, ToolError, execute_tool, run_agent


class TestTools(unittest.TestCase):
    def test_add(self):
        self.assertEqual(execute_tool("add", {"a": 2, "b": 3}), 5)

    def test_multiply(self):
        self.assertEqual(execute_tool("multiply", {"a": 6, "b": 7}), 42)

    def test_unknown_tool_rejected(self):
        with self.assertRaises(ToolError):
            execute_tool("shell", {"a": 1, "b": 2})

    def test_bad_schema_rejected(self):
        with self.assertRaises(ToolError):
            execute_tool("add", {"a": 1})

    def test_bool_rejected(self):
        with self.assertRaises(ToolError):
            execute_tool("add", {"a": True, "b": 2})


class TestLoop(unittest.TestCase):
    def test_happy_path(self):
        r = run_agent(SimulatedPlanner())
        self.assertEqual(r["status"], "completed")
        self.assertIn("42", r["answer"])

    def test_budget_exhaustion(self):
        r = run_agent(SimulatedPlanner(), max_steps=1)
        self.assertEqual(r["status"], "budget_exhausted")

    def test_zero_budget_is_invalid(self):
        with self.assertRaises(ValueError):
            run_agent(SimulatedPlanner(), max_steps=0)

    def test_unknown_tool_fails_fast(self):
        class BadPlanner:
            def next(self, _obs):
                return Action("shell", {"a": 1, "b": 2})

        r = run_agent(BadPlanner())
        self.assertEqual(r["status"], "tool_error")


if __name__ == "__main__":
    unittest.main()
