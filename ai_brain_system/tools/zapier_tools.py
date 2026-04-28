"""Zapier tool integration."""
from __future__ import annotations

from typing import Any

import requests


class ZapierTools:
    """Dispatch structured events to Zapier webhooks."""

    @staticmethod
    def trigger_webhook(webhook_url: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(webhook_url, json=payload, timeout=15)
        return {
            "status_code": response.status_code,
            "ok": response.ok,
            "response_text": response.text[:1000],
        }
