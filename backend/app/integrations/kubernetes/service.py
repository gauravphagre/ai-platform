"""Higher-level Kubernetes operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.integrations.kubernetes.client import KubernetesClient


@dataclass
class KubernetesService:
    client: KubernetesClient

    def restart_deployment(self, namespace: str, deployment: str) -> None:
        apps = self.client.apps_v1()
        body = {
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kubectl.kubernetes.io/restartedAt": "now"
                        }
                    }
                }
            }
        }
        apps.patch_namespaced_deployment(name=deployment, namespace=namespace, body=body)

    def scale_deployment(self, namespace: str, deployment: str, replicas: int) -> None:
        apps = self.client.apps_v1()
        body = {"spec": {"replicas": replicas}}
        apps.patch_namespaced_deployment_scale(name=deployment, namespace=namespace, body=body)

    def list_pods(self, namespace: str, label_selector: Optional[str] = None):
        core = self.client.core_v1()
        return core.list_namespaced_pod(namespace=namespace, label_selector=label_selector)

