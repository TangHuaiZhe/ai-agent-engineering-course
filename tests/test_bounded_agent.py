import unittest

from examples.bounded_agent import (
    Finish, ScriptedDecider, ToolCall, make_registry, run_agent,
)


class TestBoundedAgent(unittest.TestCase):
    def run_script(self, actions, **kwargs):
        return run_agent("test goal", ScriptedDecider(actions), make_registry(), **kwargs)

    def test_happy_path(self):
        r = self.run_script([ToolCall("multiply", {"a": 6, "b": 7}, "1"), Finish("42")])
        self.assertEqual((r.status, r.answer, r.model_calls, r.tool_executions), ("completed", "42", 2, 1))

    def test_finish_without_tools(self):
        r = self.run_script([Finish("no tool needed")], max_tool_executions=0)
        self.assertEqual(r.status, "completed")

    def test_model_budget_limit(self):
        r = self.run_script([ToolCall("add", {"a": 1, "b": 2}, "1")], max_model_calls=1)
        self.assertEqual(r.status, "model_budget_exhausted")

    def test_tool_budget_limit(self):
        r = self.run_script([ToolCall("add", {"a": 1, "b": 2}, "1")], max_tool_executions=0)
        self.assertEqual(r.status, "tool_budget_exhausted")
        self.assertEqual(r.tool_executions, 0)

    def test_unknown_tool_denied(self):
        r = self.run_script([ToolCall("shell", {"cmd": "rm -rf /"}, "1")])
        self.assertEqual(r.status, "policy_denied")

    def test_side_effect_needs_approval(self):
        notes = []
        r = run_agent("save note", ScriptedDecider([ToolCall("save_note", {"text": "hi"}, "1")]), make_registry(notes))
        self.assertEqual(r.status, "approval_required")
        self.assertEqual(notes, [])

    def test_approved_side_effect(self):
        notes = []
        r = run_agent("save note", ScriptedDecider([
            ToolCall("save_note", {"text": "hi"}, "1"), Finish("done")
        ]), make_registry(notes), approved_tools=frozenset({"save_note"}))
        self.assertEqual((r.status, notes), ("completed", ["hi"]))

    def test_duplicate_call_id_is_replayed_not_reexecuted(self):
        notes = []
        r = run_agent("save note", ScriptedDecider([
            ToolCall("save_note", {"text": "once"}, "1"),
            ToolCall("save_note", {"text": "once"}, "1"), Finish("done")
        ]), make_registry(notes), approved_tools=frozenset({"save_note"}))
        self.assertEqual((r.status, notes, r.tool_executions), ("completed", ["once"], 1))
        self.assertEqual(r.observations[0], r.observations[1])

    def test_call_id_argument_conflict(self):
        notes = []
        r = run_agent("save note", ScriptedDecider([
            ToolCall("save_note", {"text": "first"}, "same"),
            ToolCall("save_note", {"text": "second"}, "same")
        ]), make_registry(notes), approved_tools=frozenset({"save_note"}))
        self.assertEqual((r.status, notes), ("call_id_conflict", ["first"]))

    def test_invalid_argument_is_observation_not_policy_bypass(self):
        r = self.run_script([
            ToolCall("add", {"a": True, "b": 2}, "bad"),
            ToolCall("add", {"a": 1, "b": 2}, "fixed"), Finish("3"),
        ])
        self.assertEqual(r.status, "completed")
        self.assertEqual(r.observations[0].error_code, "invalid_arguments")
        self.assertEqual(r.observations[1].value, 3)

    def test_malformed_call_has_no_effect(self):
        r = self.run_script([ToolCall("add", {"a": 1, "b": 2}, "")])
        self.assertEqual(r.status, "invalid_decision")
        self.assertEqual(r.tool_executions, 0)

    def test_nonserializable_args_have_no_effect(self):
        r = self.run_script([ToolCall("add", {"a": {1, 2}, "b": 2}, "1")])
        self.assertEqual(r.status, "invalid_decision")

    def test_unexpected_tool_exception_is_redacted(self):
        from examples.bounded_agent import ToolRegistry, ToolSpec
        registry = ToolRegistry()

        def bad_handler(_args):
            raise RuntimeError("secret-key-should-not-leak")

        registry.register("fail", ToolSpec(bad_handler, lambda _a: None))
        r = run_agent("test", ScriptedDecider([ToolCall("fail", {}, "1"), Finish("failed")]), registry)
        self.assertEqual(r.status, "completed")
        self.assertEqual(r.observations[0].error_code, "tool_failed")
        self.assertNotIn("secret-key", repr(r))

    def test_planner_error_fails_closed(self):
        r = self.run_script([], max_model_calls=1)
        self.assertEqual(r.status, "planner_error")

    def test_nonpositive_budget_rejected(self):
        with self.assertRaises(ValueError):
            self.run_script([Finish("hi")], max_model_calls=0)


if __name__ == "__main__":
    unittest.main()
