"""Remediation agent."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RemediationAgent:
    """Agent that proposes remediation actions."""

    async def propose(self, incident_summary: str) -> list[str]:
        # TODO: integrate workflows + llm service + tool schemas
        return []

