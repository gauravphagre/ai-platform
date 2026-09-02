"""MCP tool registry.

Central registry for MCP-exposed tools. Keeps metadata separate from execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.mcp.schemas.tool_schema import MCPToolDefinition


@dataclass
class MCPToolRegistry:
    """In-memory registry for MCP tool definitions."""

    _tools: dict[str, MCPToolDefinition] = field(default_factory=dict)

    def register(self, tool: MCPToolDefinition) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> MCPToolDefinition | None:
        return self._tools.get(name)

    def list_tools(self) -> list[MCPToolDefinition]:
        return list(self._tools.values())

