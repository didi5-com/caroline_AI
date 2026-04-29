"""Taskade integration placeholder."""
from __future__ import annotations

from typing import Any


class TaskadeIntegration:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def push_update(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"status": "not_implemented", "payload": payload}

    def fetch_tasks(self, project_id: str) -> dict[str, Any]:
        return {"status": "not_implemented", "project_id": project_id}
