"""Remediation agent.

Responsible for proposing and (optionally) executing remediation actions.
Execution should go through tools/integrations with policy enforcement.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RemediationAgent:
    """Agent that proposes remediation actions."""

    async def propose(self, incident_summary: str) -> list[str]:
        # TODO: integrate workflows + llm service + tool schemas
        return []

