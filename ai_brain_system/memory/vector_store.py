"""Lightweight vector-store abstraction.

Uses a deterministic hash-embedding fallback to keep the project runnable
without heavyweight ML dependencies, while preserving an interchangeable API.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass


@dataclass
class VectorRecord:
    record_id: str
    text: str
    vector: list[float]


class VectorStore:
    """In-memory vector storage with cosine similarity search."""

    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions
        self._records: list[VectorRecord] = []

    def _embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        repeated = (digest * ((self.dimensions // len(digest)) + 1))[: self.dimensions]
        return [b / 255.0 for b in repeated]

    @staticmethod
    def _cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b, strict=False))
        an = math.sqrt(sum(x * x for x in a))
        bn = math.sqrt(sum(y * y for y in b))
        if an == 0.0 or bn == 0.0:
            return 0.0
        return dot / (an * bn)

    def add(self, record_id: str, text: str) -> None:
        self._records.append(VectorRecord(record_id=record_id, text=text, vector=self._embed(text)))

    def search(self, query: str, k: int = 5) -> list[dict[str, str | float]]:
        qv = self._embed(query)
        scored = [
            {
                "record_id": item.record_id,
                "text": item.text,
                "score": self._cosine(qv, item.vector),
            }
            for item in self._records
        ]
        scored.sort(key=lambda x: float(x["score"]), reverse=True)
        return scored[:k]
