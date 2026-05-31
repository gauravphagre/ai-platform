"""Backward-compatible Kubernetes service import."""

from app.integrations.kubernetes.service import KubernetesService as ClusterService

__all__ = ["ClusterService"]
