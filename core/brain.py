"""Brain orchestration layer."""
from __future__ import annotations

from core.agent import Agent
from core.reasoning import ReasoningEngine
from memory.long_term import LongTermMemory
from memory.short_term import ShortTermMemory


class Brain:
    def __init__(self) -> None:
        self.agent = Agent()
        self.reasoning = ReasoningEngine()
        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory()

    def process(self, user_id: str, message: str) -> str:
        # 1) Store short-term context.
        self.short_memory.add(user_id, message)

        # 2) Retrieve long-term memory context.
        long_context = self.long_memory.search(message)

        # 3) Build full context.
        context = {
            "short": self.short_memory.get(user_id),
            "long": long_context,
        }

        # 4) Decide what to do.
        decision = self.reasoning.decide(message, context)

        # 5) Execute action or chat.
        result = self.agent.execute(decision, message, context)

        # 6) Save to long-term memory.
        self.long_memory.store(message, result)

        return result

    def memory(self, user_id: str, limit: int = 10) -> dict:
        return {
            "short": self.short_memory.get(user_id),
            "long": self.long_memory.search("", top_k=limit),
        }

    def trigger_action(self, action: str, payload: dict) -> str:
        decision = {"type": "tool", "tool": action, "args": payload}
        return self.agent.execute(decision, payload.get("message", ""), {"short": [], "long": []})
