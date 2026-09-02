"""Prometheus service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.integrations.prometheus.client import PrometheusClient


@dataclass
class PrometheusService:
    client: PrometheusClient

    async def query(self, promql: str, time: Optional[str] = None) -> dict[str, Any]:
        return await self.client.query(promql=promql, time=time)

    async def query_range(
        self,
        promql: str,
        start: str,
        end: str,
        step: str = "30s",
    ) -> dict[str, Any]:
        return await self.client.query_range(promql=promql, start=start, end=end, step=step)

