import tempfile
import unittest
from pathlib import Path

from examples.workflow_lab import Workflow, WorkflowError


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "checkpoint.sqlite3"
        self.workflow = Workflow(self.path)

    def tearDown(self):
        self.workflow.close()
        self.temp.cleanup()

    def test_route_parallel_merge_and_bounded_evaluation(self):
        self.workflow.start("full", "研究虚构公司风险")
        self.assertEqual(self.workflow.resume("full"), "waiting_approval")
        data = self.workflow.state("full")[1]
        self.assertEqual(data["route"], "full")
        self.assertEqual([e["source_id"] for e in data["evidence"]], ["SIM-COMPANY-2026", "SIM-RISK-2026"])
        self.assertEqual(data["evaluation_attempts"], 2)
        self.assertEqual(self.workflow.source_calls, {"company": 1, "risk": 1})
        self.assertIsNone(self.workflow.report("full"))

    def test_summary_route_only_fetches_one_source(self):
        self.workflow.start("short", "研究虚构公司")
        self.workflow.resume("short")
        self.assertEqual(self.workflow.state("short")[1]["route"], "summary")
        self.assertEqual(self.workflow.source_calls, {"company": 1})

    def test_retry_transient_source_failure(self):
        self.workflow.fail_once.add("risk")
        self.workflow.start("retry", "研究风险")
        self.assertEqual(self.workflow.resume("retry"), "waiting_approval")
        self.assertEqual(self.workflow.source_calls["risk"], 2)

    def test_failed_source_stays_at_last_checkpoint_then_resumes(self):
        original = self.workflow._fetch
        def unavailable(key):
            if key == "risk":
                raise RuntimeError("source unavailable")
            return original(key)
        self.workflow._fetch = unavailable
        self.workflow.start("recover", "研究风险")
        with self.assertRaises(RuntimeError):
            self.workflow.resume("recover")
        self.assertEqual(self.workflow.state("recover")[0], "routed")
        self.workflow._fetch = original
        self.assertEqual(self.workflow.resume("recover"), "waiting_approval")

    def test_checkpoint_reopen_approval_and_idempotent_write(self):
        self.workflow.start("persist", "研究风险")
        self.workflow.resume("persist")
        self.workflow.close()
        self.workflow = Workflow(self.path)
        self.assertEqual(self.workflow.resume("persist"), "waiting_approval")
        self.assertEqual(self.workflow.source_calls, {})
        self.workflow.approve("persist", decision=True, reviewer="teacher")
        with self.assertRaisesRegex(RuntimeError, "simulated_crash"):
            self.workflow.resume("persist", crash_after_write=True)
        self.workflow.close()
        self.workflow = Workflow(self.path)
        self.assertEqual(self.workflow.resume("persist"), "done")
        self.assertEqual(self.workflow.report_count("persist"), 1)
        self.assertIn("SIM-RISK-2026", self.workflow.report("persist"))

    def test_rejection_never_writes_report(self):
        self.workflow.start("reject", "研究风险")
        self.workflow.resume("reject")
        self.workflow.approve("reject", decision=False, reviewer="teacher")
        self.assertEqual(self.workflow.resume("reject"), "done")
        self.assertEqual(self.workflow.report_count("reject"), 0)

    def test_approval_boundary_and_run_id_conflict(self):
        self.workflow.start("one", "研究风险")
        with self.assertRaises(WorkflowError):
            self.workflow.approve("one", decision=True, reviewer="teacher")
        with self.assertRaises(WorkflowError):
            self.workflow.start("one", "另一请求")
        self.workflow.resume("one")
        with self.assertRaises(WorkflowError):
            self.workflow.approve("one", decision=True, reviewer=" ")
        self.workflow.approve("one", decision=True, reviewer="teacher")
        with self.assertRaises(WorkflowError):
            self.workflow.approve("one", decision=True, reviewer="teacher")


if __name__ == "__main__":
    unittest.main()
