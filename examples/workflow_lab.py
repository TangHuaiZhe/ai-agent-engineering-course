"""Deterministic, resumable teaching workflow; fictional sources only.

Run with: python3 -m examples.workflow_lab
The SQLite file is a local teaching checkpoint, not a distributed transaction system.
"""

from __future__ import annotations

import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


SOURCES = {
    "company": ("SIM-COMPANY-2026", "虚构公司营收为 100 模拟单位。"),
    "risk": ("SIM-RISK-2026", "虚构公司存在供应链风险。"),
}
STAGES = ("new", "routed", "gathered", "evaluated", "waiting_approval", "approved", "done")


class WorkflowError(ValueError):
    pass


class TransientSourceError(RuntimeError):
    pass


class Workflow:
    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, request TEXT NOT NULL, stage TEXT NOT NULL, data TEXT NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS reports (run_id TEXT PRIMARY KEY REFERENCES runs(id), body TEXT NOT NULL)")
        self.db.commit()
        self.source_calls: dict[str, int] = {}
        self.fail_once: set[str] = set()

    def close(self):
        self.db.close()

    def start(self, run_id: str, request: str):
        if not run_id or not request.strip():
            raise WorkflowError("invalid_request")
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO runs VALUES (?, ?, 'new', '{}')", (run_id, request))
        row = self.db.execute("SELECT request FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row[0] != request:
            raise WorkflowError("run_id_conflict")

    def state(self, run_id: str) -> tuple[str, dict]:
        row = self.db.execute("SELECT stage, data FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            raise WorkflowError("unknown_run")
        return row[0], json.loads(row[1])

    def _advance(self, run_id: str, expected: str, next_stage: str, data: dict):
        with self.db:
            changed = self.db.execute(
                "UPDATE runs SET stage = ?, data = ? WHERE id = ? AND stage = ?",
                (next_stage, json.dumps(data, ensure_ascii=False, sort_keys=True), run_id, expected),
            ).rowcount
            if changed != 1:
                raise WorkflowError("stale_checkpoint")

    def _fetch(self, key: str) -> dict:
        self.source_calls[key] = self.source_calls.get(key, 0) + 1
        if key in self.fail_once:
            self.fail_once.remove(key)
            raise TransientSourceError(key)
        source_id, fact = SOURCES[key]
        return {"source_id": source_id, "fact": fact}

    def _fetch_with_retry(self, key: str) -> dict:
        for attempt in range(2):
            try:
                return self._fetch(key)
            except TransientSourceError:
                if attempt == 1:
                    raise
        raise AssertionError("unreachable")

    def resume(self, run_id: str, *, crash_after_write: bool = False) -> str:
        """Advance to an approval boundary or completion; safe to call again."""
        while True:
            stage, data = self.state(run_id)
            if stage in ("waiting_approval", "done"):
                return stage
            if stage == "new":
                request = self.db.execute("SELECT request FROM runs WHERE id = ?", (run_id,)).fetchone()[0]
                route = "full" if "风险" in request else "summary"
                self._advance(run_id, stage, "routed", {"route": route})
            elif stage == "routed":
                keys = ("company", "risk") if data["route"] == "full" else ("company",)
                with ThreadPoolExecutor(max_workers=len(keys)) as pool:
                    results = list(pool.map(self._fetch_with_retry, keys))
                data["evidence"] = results  # map preserves input order, regardless of finish order
                self._advance(run_id, stage, "gathered", data)
            elif stage == "gathered":
                evidence = data["evidence"]
                if not evidence or any(item["source_id"] not in {v[0] for v in SOURCES.values()} for item in evidence):
                    raise WorkflowError("invalid_evidence")
                # A bounded evaluator–optimizer: first draft has no citations; one revision adds them.
                draft = " ".join(item["fact"] for item in evidence)
                attempts = 1
                if not all(item["source_id"] in draft for item in evidence):
                    draft = " ".join(f'{item["fact"]} [{item["source_id"]}]' for item in evidence)
                    attempts += 1
                if not all(item["source_id"] in draft for item in evidence):
                    raise WorkflowError("evaluation_failed")
                data.update({"draft": draft, "evaluation_attempts": attempts})
                self._advance(run_id, stage, "evaluated", data)
            elif stage == "evaluated":
                self._advance(run_id, stage, "waiting_approval", data)
            elif stage == "approved":
                # Checkpoint and side effect share a transaction. A crash after commit replays neither.
                with self.db:
                    self.db.execute("INSERT OR IGNORE INTO reports VALUES (?, ?)", (run_id, data["draft"]))
                    changed = self.db.execute(
                        "UPDATE runs SET stage = 'done' WHERE id = ? AND stage = 'approved'", (run_id,)
                    ).rowcount
                    if changed != 1:
                        raise WorkflowError("stale_checkpoint")
                if crash_after_write:
                    raise RuntimeError("simulated_crash_after_commit")
            else:
                raise WorkflowError("invalid_stage")

    def approve(self, run_id: str, *, decision: bool, reviewer: str):
        stage, data = self.state(run_id)
        if stage != "waiting_approval" or not reviewer.strip():
            raise WorkflowError("approval_not_allowed")
        if not decision:
            data["rejected_by"] = reviewer
            self._advance(run_id, stage, "done", data)
            return
        data["approved_by"] = reviewer
        self._advance(run_id, stage, "approved", data)

    def report(self, run_id: str) -> str | None:
        row = self.db.execute("SELECT body FROM reports WHERE run_id = ?", (run_id,)).fetchone()
        return row[0] if row else None

    def report_count(self, run_id: str) -> int:
        return self.db.execute("SELECT COUNT(*) FROM reports WHERE run_id = ?", (run_id,)).fetchone()[0]


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        workflow = Workflow(Path(directory) / "checkpoint.sqlite3")
        workflow.start("demo", "研究虚构公司与风险")
        print("pause:", workflow.resume("demo"))
        print("evidence:", workflow.state("demo")[1]["evidence"])
        workflow.approve("demo", decision=True, reviewer="demo-reviewer")
        print("resume:", workflow.resume("demo"))
        print("report:", workflow.report("demo"))
        workflow.close()
