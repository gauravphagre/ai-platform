"""Loki service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.integrations.loki.client import LokiClient


@dataclass
class LokiService:
    client: LokiClient

    async def query_logs(self, logql: str, limit: int = 100) -> dict[str, Any]:
        return await self.client.query(logql=logql, limit=limit)

    async def query_logs_range(
        self,
        logql: str,
        start_ns: str,
        end_ns: str,
        step: str = "1s",
        limit: int = 1000,
    ) -> dict[str, Any]:
        return await self.client.query_range(
            logql=logql,
            start_ns=start_ns,
            end_ns=end_ns,
            step=step,
            limit=limit,
        )

