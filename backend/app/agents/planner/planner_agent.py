"""Planner agent."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlannerAgent:
    """Agent that plans multi-agent workflows."""

    async def plan(self, task: str) -> list[str]:
        # TODO: integrate LLMService with structured agent routing
        return []

