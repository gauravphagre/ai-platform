"""Prometheus HTTP client.

Uses the Prometheus HTTP API.
Docs: https://prometheus.io/docs/prometheus/latest/querying/api/
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import httpx


@dataclass
class PrometheusClient:
    base_url: str
    timeout_seconds: float = 10.0

    async def query(self, promql: str, time: Optional[str] = None) -> dict[str, Any]:
        """Execute an instant query."""
        params: dict[str, Any] = {"query": promql}
        if time is not None:
            params["time"] = time

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            resp = await client.get(f"{self.base_url.rstrip('/')}/api/v1/query", params=params)
            resp.raise_for_status()
            return resp.json()

    async def query_range(
        self,
        promql: str,
        start: str,
        end: str,
        step: str = "30s",
    ) -> dict[str, Any]:
        """Execute a range query."""
        params = {"query": promql, "start": start, "end": end, "step": step}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            resp = await client.get(
                f"{self.base_url.rstrip('/')}/api/v1/query_range",
                params=params,
            )
            resp.raise_for_status()
            return resp.json()

