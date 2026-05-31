"""MCP client abstraction.

Thin client for interacting with MCP servers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class MCPClient:
    """Minimal MCP client placeholder."""

    server_name: str

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        return {
            "server": self.server_name,
            "tool": tool_name,
            "arguments": arguments,
            "status": "not_implemented",
        }

