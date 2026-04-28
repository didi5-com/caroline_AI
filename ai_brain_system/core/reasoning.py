"""Reasoning layer for intent analysis and action planning."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReasoningDecision:
    """Structured decision from the reasoning stage."""

    intent: str
    should_store_memory: bool
    should_use_tool: bool
    tool_name: str | None = None


class Reasoner:
    """Rule-based planner with a stable contract for future LLM planners."""

    def decide(self, message: str) -> ReasoningDecision:
        lower = message.lower().strip()

        if any(kw in lower for kw in ["zapier", "webhook", "automation"]):
            return ReasoningDecision(
                intent="automation",
                should_store_memory=True,
                should_use_tool=True,
                tool_name="zapier",
            )

        if any(kw in lower for kw in ["remember", "note this", "save this", "store this"]):
            return ReasoningDecision(
                intent="memory_store",
                should_store_memory=True,
                should_use_tool=False,
            )

        return ReasoningDecision(
            intent="conversation",
            should_store_memory=True,
            should_use_tool=False,
        )
