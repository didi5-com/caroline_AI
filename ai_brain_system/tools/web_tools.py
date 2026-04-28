"""Web tool stubs for search/scrape extension."""
from __future__ import annotations

import requests


class WebTools:
    @staticmethod
    def fetch_url(url: str, timeout: int = 10) -> dict[str, str | int]:
        response = requests.get(url, timeout=timeout)
        return {"status_code": response.status_code, "text": response.text[:2000]}
