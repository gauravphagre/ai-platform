"""Workflow registry.

Central place to register workflows by name.
"""

from __future__ import annotations

from typing import Callable, Any

from app.workflows.incident_response.graph import build_incident_workflow


WORKFLOW_BUILDERS: dict[str, Callable[[], Any]] = {
    "incident_response": build_incident_workflow,
}

