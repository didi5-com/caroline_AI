"""Agent layer with LangChain-compatible design."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

try:
    from langchain_core.tools import Tool
except ImportError:  # pragma: no cover - optional dependency
    Tool = None  # type: ignore[assignment]

from ai_brain_system.config.prompts import SYSTEM_PROMPT


@dataclass
class AgentResult:
    response: str
    used_tool: str | None = None
    tool_output: dict[str, Any] | None = None


class BrainAgent:
    """Encapsulates multi-step decision and tool-calling behavior."""

    def __init__(self, available_tools: dict[str, Callable[..., dict[str, Any]]]) -> None:
        self.available_tools = available_tools
        self.system_prompt = SYSTEM_PROMPT

    def run(
        self,
        user_input: str,
        context: list[dict[str, Any]],
        selected_tool: str | None = None,
        tool_args: dict[str, Any] | None = None,
    ) -> AgentResult:
        if selected_tool:
            tool_fn = self.available_tools.get(selected_tool)
            if not tool_fn:
                return AgentResult(response=f"Requested tool '{selected_tool}' is not registered.")

            output = tool_fn(**(tool_args or {}))
            return AgentResult(
                response=f"Executed tool '{selected_tool}' successfully.",
                used_tool=selected_tool,
                tool_output=output,
            )

        recent = context[0]["content"] if context and "content" in context[0] else "No memory yet."
        response = (
            "Intent processed. Memory checked. "
            f"Most recent memory: {recent}. "
            "No external action was required, so I responded directly."
        )
        return AgentResult(response=response)

    def build_langchain_tool_specs(self) -> list[Any]:
        if Tool is None:
            return []

        return [Tool(name=name, func=fn, description=f"AI Brain tool: {name}") for name, fn in self.available_tools.items()]
