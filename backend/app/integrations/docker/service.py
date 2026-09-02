"""Docker service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.integrations.docker.client import DockerClient


@dataclass
class DockerService:
    client: DockerClient

    @classmethod
    def from_base_url(cls, base_url: Optional[str] = None) -> "DockerService":
        return cls(client=DockerClient(base_url=base_url))

    def restart_container(self, container_name: str, timeout: int = 10) -> None:
        client = self.client.get_client()
        container = client.containers.get(container_name)
        container.restart(timeout=timeout)

    def list_containers(self, all: bool = False):
        client = self.client.get_client()
        return client.containers.list(all=all)

