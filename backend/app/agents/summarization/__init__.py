"""Summarization agent.

Responsible for summarizing conversations, incidents, and workflow runs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SummaryAgent:
    """Agent that summarizes text."""

    async def summarize(self, text: str, max_chars: int = 2000) -> str:
        # TODO: integrate LLMService with structured schemas
        return text[:max_chars]

