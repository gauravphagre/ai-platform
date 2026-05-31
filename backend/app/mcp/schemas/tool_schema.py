"""Schemas for MCP tool definitions."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class MCPToolParameter(BaseModel):
    """Single MCP tool parameter definition."""

    name: str
    type: Literal["string", "number", "integer", "boolean", "object", "array"]
    description: str
    required: bool = False
    default: Any = None


class MCPToolDefinition(BaseModel):
    """Metadata describing an MCP-exposed tool."""

    name: str
    description: str
    parameters: list[MCPToolParameter] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

