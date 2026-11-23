"""A dependency-free teaching implementation of a bounded Agent runner.

This is NOT an LLM; ScriptedDecider stands in for model output. The host code,
not the model, enforces tool permissions, budgets and call_id replay handling.

Run from repository root: python3 examples/bounded_agent.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


class ToolInputError(ValueError):
    """A recoverable validation failure. Never include secrets here."""


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]
    call_id: str


@dataclass(frozen=True)
class Finish:
    answer: str


Decision = ToolCall | Finish


@dataclass(frozen=True)
class Observation:
    call_id: str
    tool_name: str
    ok: bool
    value: Any = None
    error_code: str | None = None


@dataclass(frozen=True)
class TraceEvent:
    kind: str
    detail: str  # Deliberately excludes raw tool arguments and tool outputs.


@dataclass(frozen=True)
class AgentState:
    goal: str
    observations: tuple[Observation, ...]


@dataclass(frozen=True)
class RunResult:
    status: str
    answer: str | None
    model_calls: int
    tool_executions: int
    observations: tuple[Observation, ...]
    trace: tuple[TraceEvent, ...]


class Decider(Protocol):
    def decide(self, state: AgentState) -> Decision: ...


@dataclass(frozen=True)
class ToolSpec:
    handler: Callable[[dict[str, Any]], Any]
    validator: Callable[[dict[str, Any]], None]
    requires_approval: bool = False


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, name: str, spec: ToolSpec) -> None:
        if not name or name in self._tools:
            raise ValueError("Tool name must be nonempty and unique")
        self._tools[name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)


def integer_pair(arguments: dict[str, Any]) -> None:
    if set(arguments) != {"a", "b"}:
        raise ToolInputError("Expected exactly the keys a and b")
    if any(type(arguments[key]) is not int for key in ("a", "b")):
        raise ToolInputError("Both arguments must be integers, not booleans")


def note_text(arguments: dict[str, Any]) -> None:
    if set(arguments) != {"text"} or not isinstance(arguments["text"], str):
        raise ToolInputError("Expected exactly one string field: text")
    if not 0 < len(arguments["text"]) <= 200:
        raise ToolInputError("Note length must be between 1 and 200 characters")


def make_registry(notes: list[str] | None = None) -> ToolRegistry:
    """The write tool uses an in-memory list to demonstrate an action side effect."""
    if notes is None:
        notes = []
    registry = ToolRegistry()
    registry.register("add", ToolSpec(lambda args: args["a"] + args["b"], integer_pair))
    registry.register("multiply", ToolSpec(lambda args: args["a"] * args["b"], integer_pair))

    def save_note(args: dict[str, Any]) -> str:
        notes.append(args["text"])
        return "saved"

    registry.register("save_note", ToolSpec(save_note, note_text, requires_approval=True))
    return registry


def _fingerprint(call: ToolCall) -> str:
    return json.dumps([call.name, call.arguments], sort_keys=True, ensure_ascii=False, allow_nan=False)


def run_agent(
    goal: str,
    decider: Decider,
    registry: ToolRegistry,
    *,
    max_model_calls: int = 6,
    max_tool_executions: int = 4,
    approved_tools: frozenset[str] = frozenset(),
) -> RunResult:
    """Execute one tool call per model decision, safely bounded for teaching.

    Results are replayed for identical call_ids in this run. This is NOT durable
    exactly-once processing; production systems need persisted execution records.
    """
    if max_model_calls < 1 or max_tool_executions < 0:
        raise ValueError("Invalid execution budget")
    observations: list[Observation] = []
    trace: list[TraceEvent] = []
    seen: dict[str, tuple[str, Observation]] = {}
    executions = 0
    calls = 0

    def result(status: str, answer: str | None = None) -> RunResult:
        trace.append(TraceEvent("terminal", status))
        return RunResult(status, answer, calls, executions, tuple(observations), tuple(trace))

    for _ in range(max_model_calls):
        calls += 1
        state = AgentState(goal, tuple(observations))
        try:
            action = decider.decide(state)
        except Exception:  # Host should record details in protected logs, not model-visible output.
            trace.append(TraceEvent("planner_error", "decider raised an exception"))
            return result("planner_error")

        if isinstance(action, Finish):
            trace.append(TraceEvent("finish", "model produced final answer (not fact-checked)"))
            return result("completed", action.answer)
        if not isinstance(action, ToolCall):
            return result("invalid_decision")
        if (
            not isinstance(action.name, str)
            or not isinstance(action.call_id, str)
            or not action.call_id.strip()
            or not isinstance(action.arguments, dict)
        ):
            return result("invalid_decision")
        try:
            fingerprint = _fingerprint(action)
        except (TypeError, ValueError):
            return result("invalid_decision")

        # Reject unauthorized requests BEFORE checking or executing effects.
        spec = registry.get(action.name)
        if spec is None:
            trace.append(TraceEvent("policy", "unknown tool denied"))
            return result("policy_denied")
        if spec.requires_approval and action.name not in approved_tools:
            trace.append(TraceEvent("policy", "side-effect tool needs approval"))
            return result("approval_required")

        if action.call_id in seen:
            old_fingerprint, old_observation = seen[action.call_id]
            if fingerprint != old_fingerprint:
                return result("call_id_conflict")
            observations.append(old_observation)
            trace.append(TraceEvent("replay", f"{action.name} reused cached result"))
            continue

        if executions >= max_tool_executions:
            return result("tool_budget_exhausted")
        # Count attempted handler executions, including input failures and exceptions.
        executions += 1
        try:
            spec.validator(action.arguments)
            value = spec.handler(action.arguments)
            observation = Observation(action.call_id, action.name, True, value=value)
        except ToolInputError:
            observation = Observation(action.call_id, action.name, False, error_code="invalid_arguments")
        except Exception:
            observation = Observation(action.call_id, action.name, False, error_code="tool_failed")

        seen[action.call_id] = (fingerprint, observation)
        observations.append(observation)
        trace.append(TraceEvent("tool_result", f"{action.name}: {'ok' if observation.ok else observation.error_code}"))

    return result("model_budget_exhausted")


class ScriptedDecider:
    """Deterministic decisions for tests and teaching; no LLM API call."""

    def __init__(self, decisions: list[Decision]):
        self._decisions = iter(decisions)

    def decide(self, state: AgentState) -> Decision:
        return next(self._decisions)


if __name__ == "__main__":
    result = run_agent(
        "6 × 7 是多少？",
        ScriptedDecider([ToolCall("multiply", {"a": 6, "b": 7}, "calc-1"), Finish("结果是 42")]),
        make_registry(),
    )
    print({"status": result.status, "answer": result.answer, "model_calls": result.model_calls,
           "tool_executions": result.tool_executions, "trace": [e.kind for e in result.trace]})
