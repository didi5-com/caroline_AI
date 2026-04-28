"""Persistent semantic vector memory via OpenAI embeddings + FAISS."""
from __future__ import annotations

import faiss
import numpy as np
from openai import OpenAI

from config.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


class VectorStore:
    def __init__(self, dimension: int = 1536) -> None:
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts: list[str] = []

    def _embed(self, text: str) -> np.ndarray:
        response = client.embeddings.create(model="text-embedding-3-small", input=text)
        return np.array(response.data[0].embedding, dtype=np.float32)

    def add(self, text: str) -> None:
        vector = self._embed(text)
        self.index.add(np.array([vector]))
        self.texts.append(text)

    def search(self, query: str, top_k: int = 5) -> list[str]:
        if len(self.texts) == 0:
            return []

        query_vec = self._embed(query).reshape(1, -1)
        distances, indices = self.index.search(query_vec, top_k)

        _ = distances  # reserved for score-aware ranking in future iterations
        results: list[str] = []
        for idx in indices[0]:
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx])

        return results
