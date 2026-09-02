"""Base agent interface.

This is intentionally minimal to avoid changing existing agent behavior.
"""

from __future__ import annotations

from abc import ABC


class Agent(ABC):
    """Base class for all agents."""

    name: str = "agent"

