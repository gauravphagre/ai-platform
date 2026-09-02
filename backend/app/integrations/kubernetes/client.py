"""Kubernetes client wrapper.

This is a thin wrapper around the official Kubernetes Python client.
We keep it optional to avoid forcing the dependency in minimal deployments.

If kubernetes package is not installed, methods will raise RuntimeError.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class KubernetesClient:
    context: Optional[str] = None
    in_cluster: bool = False

    def _load(self) -> Any:
        try:
            from kubernetes import client as k8s_client  # type: ignore
            from kubernetes import config as k8s_config  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError(
                "Kubernetes integration requires 'kubernetes' package."
            ) from e

        if self.in_cluster:
            k8s_config.load_incluster_config()
        else:
            k8s_config.load_kube_config(context=self.context)

        return k8s_client

    def core_v1(self):
        k8s_client = self._load()
        return k8s_client.CoreV1Api()

    def apps_v1(self):
        k8s_client = self._load()
        return k8s_client.AppsV1Api()

