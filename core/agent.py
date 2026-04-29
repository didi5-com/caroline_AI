"""LLM + tool execution loop for Caroline AI."""
from __future__ import annotations

from config.settings import MODEL
from core.llm_client import get_openai_client
from tools import file_tools, system_tools, web_tools, zapier_tools

from openai import OpenAI

from config.settings import MODEL, OPENAI_API_KEY
from tools import file_tools, system_tools, web_tools, zapier_tools

client = OpenAI(api_key=OPENAI_API_KEY)


class Agent:
    def __init__(self) -> None:
        self.tools = {
            "run_command": system_tools.run_command,
            "open_app": system_tools.open_app,
            "read_file": file_tools.read_file,
            "write_file": file_tools.write_file,
            "web_search": web_tools.search,
            "zapier": zapier_tools.trigger,
        }

    def execute(self, decision: dict, message: str, context: dict) -> str:
        if decision.get("type") == "chat":
            if decision.get("response"):
                return str(decision["response"])
            return self._final_response(message, context)

        if decision.get("type") == "tool":
            tool_name = decision.get("tool")
            args = decision.get("args", {})
            tool = self.tools.get(tool_name)

            if tool:
                try:
                    tool_result = tool(**args)
                except Exception as exc:  # noqa: BLE001
                    tool_result = f"Tool execution failed: {exc}"

                return self._final_response(message, context, str(tool_result))
                return self._final_response(message, context, tool_result)

            return f"Tool not found: {tool_name}"

        return "Invalid decision"

    def _final_response(self, message: str, context: dict, tool_result: str | None = None) -> str:
        client = get_openai_client()
        if client is None:
            return f"[Offline Caroline] {message}"

        prompt = (
            "You are Caroline AI.\n"
            f"User message: {message}\n"
            f"Context: {context}\n"
            f"Tool result: {tool_result}\n"
            "Respond naturally and intelligently."
        )

        try:
            res = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            return res.choices[0].message.content or ""
        except Exception as exc:  # noqa: BLE001
            return f"[Fallback] Unable to query LLM: {exc}"
        prompt = f"""
You are Caroline AI.

User message: {message}

Context: {context}

Tool result (if any): {tool_result}

Respond naturally and intelligently.
""".strip()

        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        return res.choices[0].message.content or ""
