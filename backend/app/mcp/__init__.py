"""Model Context Protocol (MCP) package.

This package contains the platform's MCP building blocks:
- registry: tool registration and discovery
- servers: MCP server implementations
- clients: MCP client adapters
- permissions: policy enforcement for tool access
- schemas: shared MCP tool schemas
"""

from app.mcp.clients.mcp_client import MCPClient
from app.mcp.permissions.policy_engine import PolicyEngine
from app.mcp.registry.tool_registry import MCPToolRegistry
from app.mcp.schemas.tool_schema import MCPToolDefinition, MCPToolParameter

__all__ = [
    "MCPClient",
    "PolicyEngine",
    "MCPToolRegistry",
    "MCPToolDefinition",
    "MCPToolParameter",
]

