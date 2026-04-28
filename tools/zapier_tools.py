"""Zapier webhook trigger tool."""
from __future__ import annotations

import requests

from config.settings import ZAPIER_WEBHOOK_URL


def trigger(message: str) -> str:
    if not ZAPIER_WEBHOOK_URL:
        return "ZAPIER_WEBHOOK_URL is not configured"

    response = requests.post(ZAPIER_WEBHOOK_URL, json={"message": message}, timeout=15)
    return f"Zapier status={response.status_code}"
