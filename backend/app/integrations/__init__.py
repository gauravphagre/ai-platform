"""External integrations.

This package contains thin clients/services for external systems (Prometheus, Loki,
Kubernetes, GitHub, Docker). These modules should be I/O focused and provider-specific.
Business logic belongs in services/workflows.
"""

from app.integrations.prometheus.client import PrometheusClient
from app.integrations.loki.client import LokiClient
from app.integrations.kubernetes.client import KubernetesClient
from app.integrations.github.github_service import GitHubService
from app.integrations.docker.docker_service import DockerService

__all__ = [
    "PrometheusClient",
    "LokiClient",
    "KubernetesClient",
    "GitHubService",
    "DockerService",
]

