"""Long-term semantic memory using vector storage."""
from __future__ import annotations

from memory.vector_store import VectorStore


class LongTermMemory:
    def __init__(self) -> None:
        self.vector = VectorStore()

    def store(self, text: str, response: str) -> None:
        combined = f"User: {text} | AI: {response}"
        self.vector.add(combined)

    def search(self, query: str, top_k: int = 5) -> list[str]:
        return self.vector.search(query, top_k=top_k)
