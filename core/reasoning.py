"""LLM-based decision engine for chat vs tool actions."""
from __future__ import annotations

import json

from config.settings import MODEL
from core.llm_client import get_openai_client


class ReasoningEngine:
    """LLM decides chat/tool action and structured tool arguments."""

    def decide(self, message: str, context: dict) -> dict:
        client = get_openai_client()
        if client is None:
            return {"type": "chat", "response": "API key missing; running in offline response mode."}

        system_prompt = """
You are Caroline AI's reasoning engine.
Return ONLY valid JSON:
{"type":"chat|tool","tool":"name","args":{},"response":"optional"}
Tools: run_command, web_search, read_file, write_file, zapier.
""".strip()

        user_prompt = f"User message: {message}\nContext: {context}"

        try:
            res = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            content = res.choices[0].message.content or ""
        except Exception as exc:  # noqa: BLE001
            return {"type": "chat", "response": f"Reasoning fallback due to model error: {exc}"}

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"type": "chat", "response": content}
