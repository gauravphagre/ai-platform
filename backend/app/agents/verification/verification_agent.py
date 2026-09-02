"""Verification agent."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VerificationAgent:
    """Agent that verifies responses and actions."""

    async def verify_text(self, response: str, sources: list[str] | None = None) -> bool:
        # TODO: integrate app.evals.hallucination
        return True

