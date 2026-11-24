import tempfile
import unittest
from collections import Counter
from pathlib import Path

from examples.evaluation_lab import (
    ATTACK, Case, Outcome, evaluate_version, grade, load_cases, paired_report, run_case,
)


class TestEvaluationLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases()

    def test_dataset_has_thirty_balanced_cases(self):
        self.assertEqual(len(self.cases), 30)
        self.assertEqual(set(Counter(c.category for c in self.cases).values()), {6})
        self.assertEqual(len({c.id for c in self.cases}), 30)

    def test_paired_result_exposes_improvement_and_regression(self):
        baseline, _ = evaluate_version(self.cases, "baseline")
        candidate, _ = evaluate_version(self.cases, "candidate")
        self.assertEqual(sum(x.passed for x in baseline), 24)
        self.assertEqual(sum(x.passed for x in candidate), 28)
        self.assertEqual(
            {c.case_id for c, b in zip(candidate, baseline) if c.passed and not b.passed},
            {f"I{i:02}" for i in range(1, 7)},
        )
        self.assertEqual(
            {c.case_id for c, b in zip(candidate, baseline) if not c.passed and b.passed},
            {"N05", "N06"},
        )
        report = paired_report(self.cases)
        self.assertIn("退化案例：N05, N06", report)
        self.assertIn("injection", report)

    def test_ambiguous_case_does_not_call_tool(self):
        case = next(c for c in self.cases if c.id == "A01")
        outcome = run_case(case, "candidate")
        self.assertEqual((outcome.action, outcome.tool_calls), ("clarify", 0))
        self.assertEqual(len(outcome.spans), 1)
        self.assertTrue(grade(case, outcome).passed)

    def test_missing_and_failure_are_distinct(self):
        for case_id, action in (("M01", "abstain"), ("F01", "retry_later")):
            case = next(c for c in self.cases if c.id == case_id)
            outcome = run_case(case, "candidate")
            self.assertEqual(outcome.action, action)
            self.assertTrue(grade(case, outcome).passed)

    def test_trace_has_parent_span_and_no_raw_request_or_attack(self):
        case = next(c for c in self.cases if c.id == "I01")
        outcome = run_case(case, "candidate")
        self.assertEqual([s.name for s in outcome.spans], ["route", "tool", "compose"])
        self.assertEqual(outcome.spans[0].parent_id, None)
        self.assertTrue(all(s.trace_id == "candidate:I01" for s in outcome.spans))
        self.assertTrue(all(s.parent_id == outcome.spans[0].span_id for s in outcome.spans[1:]))
        self.assertTrue(all(s.duration_ms >= 0 for s in outcome.spans))
        serialized = str(outcome.spans)
        self.assertNotIn(case.request, serialized)
        self.assertNotIn(ATTACK, serialized)

    def test_grader_rejects_bad_citation_and_injection(self):
        case = next(c for c in self.cases if c.id == "I01")
        baseline = run_case(case, "baseline")
        self.assertEqual(grade(case, baseline).reason, "untrusted_text_in_answer")
        forged = Outcome("answer", f"模拟值 [SIM-OTHER]。", "SIM-OTHER", 1, ())
        self.assertEqual(grade(case, forged).reason, "invalid_citation")
        copied = Outcome("answer", f"模拟值 [{case.source_id}]。{ATTACK}", case.source_id, 1, ())
        self.assertEqual(grade(case, copied).reason, "untrusted_text_in_answer")

    def test_dataset_validation_rejects_duplicate_and_bad_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cases.jsonl"
            path.write_text(
                '{"id":"X","category":"normal","request":"q","source_id":"SIM-X","tool_status":"ok","expected":"answer"}\n'
                '{"id":"X","category":"normal","request":"q","source_id":"SIM-X","tool_status":"ok","expected":"answer"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate_case_id"):
                load_cases(path)
            path.write_text(
                '{"id":"X","category":"missing","request":"q","source_id":"SIM-X","tool_status":"ok","expected":"answer"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid_case_contract"):
                load_cases(path)

    def test_unknown_version_rejected(self):
        with self.assertRaises(ValueError):
            run_case(self.cases[0], "unknown")
        with self.assertRaises(ValueError):
            paired_report([self.cases[0], self.cases[0]])


if __name__ == "__main__":
    unittest.main()
