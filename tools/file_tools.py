"""File tools for read/write operations."""
from __future__ import annotations

from pathlib import Path


def read_file(path: str) -> str:
    if path == "auto":
        return "Auto path resolution not configured"
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} chars to {path}"
