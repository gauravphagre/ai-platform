"""Filesystem MCP server.

Starter MCP server exposing safe filesystem-oriented capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileSystemMCPServer:
    """Minimal filesystem-backed MCP server placeholder."""

    root_path: str

    def resolve_path(self, relative_path: str) -> Path:
        return Path(self.root_path).joinpath(relative_path).resolve()

