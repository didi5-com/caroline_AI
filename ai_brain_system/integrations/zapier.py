"""Higher-level Zapier integration adapter."""
from __future__ import annotations

from typing import Any

from ai_brain_system.tools.zapier_tools import ZapierTools


class ZapierIntegration:
    def __init__(self, default_webhook_url: str | None = None) -> None:
        self.default_webhook_url = default_webhook_url

    def send_event(self, event_name: str, data: dict[str, Any], webhook_url: str | None = None) -> dict[str, Any]:
        target = webhook_url or self.default_webhook_url
        if not target:
            raise ValueError("Zapier webhook URL is not configured")

        payload = {"event": event_name, "data": data}
        return ZapierTools.trigger_webhook(target, payload)
