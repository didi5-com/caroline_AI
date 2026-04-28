"""Short-term in-memory conversation context."""
from __future__ import annotations

from collections import defaultdict, deque


class ShortTermMemory:
    def __init__(self, max_items: int = 20) -> None:
        self.max_items = max_items
        self._sessions: dict[str, deque[str]] = defaultdict(lambda: deque(maxlen=self.max_items))

    def add(self, user_id: str, message: str) -> None:
        self._sessions[user_id].append(message)

    def get(self, user_id: str) -> list[str]:
        return list(self._sessions[user_id])
