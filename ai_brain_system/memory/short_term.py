"""Session-scoped memory store."""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque


class ShortTermMemory:
    """Stores recent conversational turns per session."""

    def __init__(self, max_turns: int = 20) -> None:
        self.max_turns = max_turns
        self._sessions: dict[str, Deque[dict[str, str]]] = defaultdict(
            lambda: deque(maxlen=self.max_turns)
        )

    def add_turn(self, session_id: str, role: str, content: str) -> None:
        self._sessions[session_id].append({"role": role, "content": content})

    def get_context(self, session_id: str) -> list[dict[str, str]]:
        return list(self._sessions[session_id])

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
