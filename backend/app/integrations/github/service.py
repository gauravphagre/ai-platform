"""GitHub service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.integrations.github.client import GitHubClient


@dataclass
class GitHubService:
    client: GitHubClient

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        return await self.client.post(f"repos/{owner}/{repo}/issues", json=payload)

