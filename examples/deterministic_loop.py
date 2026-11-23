"""A dependency-free teaching example of a bounded Agent loop.

This is a simulated decision maker, NOT an LLM. Run from repo root:
    python3 examples/deterministic_loop.py
"""

from dataclasses import dataclass
from typing import Any


class ToolError(ValueError):
    """Expected tool execution failure."""


def execute_tool(name: str, arguments: dict[str, Any]) -> int:
    """Allowlist and validate all tool calls; avoid eval/exec."""
    if name not in {"add", "multiply"}:
        raise ToolError(f"Unknown tool: {name}")
    if set(arguments) != {"a", "b"}:
        raise ToolError("Tool requires exactly 'a' and 'b'")
    a, b = arguments["a"], arguments["b"]
    if type(a) is not int or type(b) is not int:
        raise ToolError("Only integers are allowed")
    return a + b if name == "add" else a * b


@dataclass
class Action:
    tool: str | None = None
    arguments: dict[str, Any] | None = None
    final: str | None = None


class SimulatedPlanner:
    """A deterministic stand-in for the LLM decision stage."""

    def next(self, observation: list[dict[str, Any]]) -> Action:
        if not observation:
            return Action("multiply", {"a": 6, "b": 7})
        return Action(final=f"Final result: {observation[-1]['result']}")


def run_agent(planner: SimulatedPlanner, max_steps: int = 5) -> dict[str, Any]:
    if max_steps <= 0:
        raise ValueError("max_steps must be positive")
    observations: list[dict[str, Any]] = []
    for step in range(max_steps):
        action = planner.next(observations)
        if action.final is not None:
            return {"status": "completed", "answer": action.final, "steps": step}
        if action.tool is None or action.arguments is None:
            return {"status": "invalid_action", "steps": step}
        try:
            value = execute_tool(action.tool, action.arguments)
        except ToolError as exc:
            return {"status": "tool_error", "error": str(exc), "steps": step + 1}
        observations.append({"tool": action.tool, "result": value})
    return {"status": "budget_exhausted", "steps": max_steps}


if __name__ == "__main__":
    print(run_agent(SimulatedPlanner()))
