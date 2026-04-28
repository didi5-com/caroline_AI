"""SQLite-backed long-term memory module."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class LongTermMemory:
    """Persist facts and events for future retrieval."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def store(self, session_id: str, content: str, metadata: str | None = None) -> int:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO memories(session_id, content, metadata, created_at) VALUES(?, ?, ?, ?)",
                (session_id, content, metadata, created_at),
            )
            conn.commit()
            return int(cur.lastrowid)

    def fetch_recent(self, session_id: str, limit: int = 10) -> list[dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, content, metadata, created_at
                FROM memories
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, limit),
            ).fetchall()
        return [
            {
                "id": row[0],
                "content": row[1],
                "metadata": row[2],
                "created_at": row[3],
            }
            for row in rows
        ]
