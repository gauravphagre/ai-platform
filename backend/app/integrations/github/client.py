"""GitHub client wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class GitHubClient:
    token: str
    base_url: str = "https://api.github.com"
    timeout_seconds: float = 10.0

    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    async def post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            resp = await client.post(
                f"{self.base_url.rstrip('/')}/{path.lstrip('/')}",
                headers=self.headers(),
                json=json,
            )
            resp.raise_for_status()
            return resp.json()

