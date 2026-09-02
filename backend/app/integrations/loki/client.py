"""Loki HTTP client.

Uses Grafana Loki HTTP API.
Docs: https://grafana.com/docs/loki/latest/api/
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import httpx


@dataclass
class LokiClient:
    base_url: str
    timeout_seconds: float = 10.0

    async def query(self, logql: str, limit: int = 100, direction: str = "BACKWARD") -> dict[str, Any]:
        """Instant query (query endpoint)."""
        params = {"query": logql, "limit": limit, "direction": direction}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            resp = await client.get(f"{self.base_url.rstrip('/')}/loki/api/v1/query", params=params)
            resp.raise_for_status()
            return resp.json()

    async def query_range(
        self,
        logql: str,
        start_ns: str,
        end_ns: str,
        step: str = "1s",
        limit: int = 1000,
        direction: str = "BACKWARD",
    ) -> dict[str, Any]:
        """Range query (query_range endpoint)."""
        params = {
            "query": logql,
            "start": start_ns,
            "end": end_ns,
            "step": step,
            "limit": limit,
            "direction": direction,
        }
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            resp = await client.get(
                f"{self.base_url.rstrip('/')}/loki/api/v1/query_range",
                params=params,
            )
            resp.raise_for_status()
            return resp.json()

