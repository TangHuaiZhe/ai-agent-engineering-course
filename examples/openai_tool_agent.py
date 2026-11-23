"""Optional real-model example using the OpenAI Responses API.

Before running, install `openai` and set OPENAI_API_KEY and OPENAI_MODEL.
It has NO dangerous tools: only validated integer arithmetic.
"""

import json
import os

from deterministic_loop import ToolError, execute_tool


def main() -> None:
    from openai import OpenAI

    model = os.environ.get("OPENAI_MODEL")
    if not model:
        raise SystemExit("Set OPENAI_MODEL to a model available to your account")

    client = OpenAI()
    tools = [
        {
            "type": "function",
            "name": name,
            "description": f"Calculate {name} of two integers.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            "strict": True,
        }
        for name in ("add", "multiply")
    ]
    history: list = [
        {"role": "user", "content": "Use the multiply tool to compute 6 * 7, then explain the result."}
    ]
    for _ in range(6):
        response = client.responses.create(model=model, input=history, tools=tools)
        history.extend(response.output)
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            print(response.output_text)
            return
        for call in calls:
            try:
                arguments = json.loads(call.arguments)
                result = execute_tool(call.name, arguments)
                output = json.dumps({"ok": True, "result": result})
            except (ToolError, ValueError, TypeError) as exc:
                output = json.dumps({"ok": False, "error": str(exc)})
            history.append({"type": "function_call_output", "call_id": call.call_id, "output": output})
    raise RuntimeError("Agent exceeded the model/tool iteration budget")


if __name__ == "__main__":
    main()
