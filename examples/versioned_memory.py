"""Teaching-only versioned memory store.

This shows supersede/delete/source-policy semantics in memory. It is NOT a
production privacy deletion system and is not durable across process restarts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

ALLOWED_SOURCES = frozenset({"explicit_user_statement", "verified_project_fact"})


@dataclass
class MemoryRecord:
    record_id: int
    key: str
    value: Any
    source: str
    version: int
    created_at: str
    status: str = "active"
    supersedes: int | None = None


class MemoryPolicyError(ValueError):
    pass


class VersionedMemory:
    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []
        self._next_id = 1

    def set(self, key: str, value: Any, *, source: str) -> MemoryRecord:
        if source not in ALLOWED_SOURCES:
            raise MemoryPolicyError("source_not_allowed")
        if not isinstance(key, str) or not key.strip():
            raise MemoryPolicyError("invalid_key")

        previous = self.current(key)
        history = self.history(key)
        version = (history[-1].version + 1) if history else 1
        supersedes = history[-1].record_id if history else None
        if previous is not None:
            previous.status = "superseded"

        record = MemoryRecord(
            record_id=self._next_id,
            key=key,
            value=value,
            source=source,
            version=version,
            created_at=datetime.now(timezone.utc).isoformat(),
            supersedes=supersedes,
        )
        self._next_id += 1
        self._records.append(record)
        return record

    def current(self, key: str) -> MemoryRecord | None:
        active = [record for record in self._records if record.key == key and record.status == "active"]
        if not active:
            return None
        if len(active) != 1:
            raise RuntimeError("memory_invariant_broken")
        return active[0]

    def delete(self, key: str) -> bool:
        record = self.current(key)
        if record is None:
            return False
        record.status = "deleted"
        return True

    def history(self, key: str) -> tuple[MemoryRecord, ...]:
        return tuple(record for record in self._records if record.key == key)


if __name__ == "__main__":
    memory = VersionedMemory()
    memory.set("preferred_editor", "Vim", source="explicit_user_statement")
    memory.set("preferred_editor", "VS Code", source="explicit_user_statement")
    print("current:", memory.current("preferred_editor"))
    print("history:", memory.history("preferred_editor"))
    memory.delete("preferred_editor")
    print("after delete:", memory.current("preferred_editor"))
