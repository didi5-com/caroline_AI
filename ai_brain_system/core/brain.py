"""Top-level orchestrator for AI Brain System."""
from __future__ import annotations

from typing import Any

from ai_brain_system.config.settings import get_settings
from ai_brain_system.core.agent import BrainAgent
from ai_brain_system.core.reasoning import Reasoner
from ai_brain_system.integrations.zapier import ZapierIntegration
from ai_brain_system.memory.long_term import LongTermMemory
from ai_brain_system.memory.short_term import ShortTermMemory
from ai_brain_system.memory.vector_store import VectorStore


class AIBrain:
    """Coordinates memory, reasoning, tools, and response generation."""

    def __init__(self) -> None:
        settings = get_settings()

        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(settings.sqlite_path)
        self.vector_store = VectorStore()

        self.reasoner = Reasoner()
        self.zapier = ZapierIntegration(settings.zapier_webhook_url)
        self.agent = BrainAgent(available_tools={"zapier": self._trigger_zapier})

    def _trigger_zapier(
        self,
        event_name: str,
        data: dict[str, Any],
        webhook_url: str | None = None,
    ) -> dict[str, Any]:
        return self.zapier.send_event(event_name=event_name, data=data, webhook_url=webhook_url)

    def execute_action(self, action_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        if action_name == "zapier":
            return self._trigger_zapier(
                event_name=payload["event_name"],
                data=payload["data"],
                webhook_url=payload.get("webhook_url"),
            )
        raise ValueError(f"Unsupported action: {action_name}")

    def process(self, session_id: str, user_input: str) -> dict[str, Any]:
        decision = self.reasoner.decide(user_input)

        short_context = self.short_term.get_context(session_id)
        long_context = self.long_term.fetch_recent(session_id, limit=5)
        semantic_hits = self.vector_store.search(user_input, k=3)
        combined_context = short_context + long_context + semantic_hits

        selected_tool = decision.tool_name if decision.should_use_tool else None
        tool_args: dict[str, Any] | None = None

        if selected_tool == "zapier":
            tool_args = {
                "event_name": "ai_brain_event",
                "data": {"session_id": session_id, "message": user_input},
            }

        result = self.agent.run(
            user_input=user_input,
            context=combined_context,
            selected_tool=selected_tool,
            tool_args=tool_args,
        )

        self.short_term.add_turn(session_id, "user", user_input)
        self.short_term.add_turn(session_id, "assistant", result.response)

        memory_id: int | None = None
        if decision.should_store_memory:
            memory_id = self.long_term.store(session_id=session_id, content=user_input, metadata=decision.intent)
            self.vector_store.add(record_id=str(memory_id), text=user_input)

        return {
            "intent": decision.intent,
            "response": result.response,
            "used_tool": result.used_tool,
            "tool_output": result.tool_output,
            "stored_memory_id": memory_id,
            "memory_context": {
                "short_term_turns": len(short_context),
                "long_term_items": len(long_context),
                "semantic_hits": len(semantic_hits),
            },
        }
