"""Docker client wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DockerClient:
    base_url: Optional[str] = None

    def get_client(self) -> Any:
        try:
            import docker  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError("Docker integration requires 'docker' package.") from e

        if self.base_url:
            return docker.DockerClient(base_url=self.base_url)
        return docker.from_env()

