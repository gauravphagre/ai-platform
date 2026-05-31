"""MCP policy engine.

Evaluates whether a caller is allowed to invoke a given MCP tool.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PolicyEngine:
    """Simple allow-list policy engine."""

    allowed_tools: set[str] = field(default_factory=set)

    def is_allowed(self, tool_name: str) -> bool:
        if not self.allowed_tools:
            return True
        return tool_name in self.allowed_tools

