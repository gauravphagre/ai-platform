"""
Incident Response Workflow

Autonomous workflow for detecting, analyzing, and remediating incidents.

Flow:
1. Retrieve logs from observability system
2. Retrieve metrics from monitoring system
3. Analyze root cause using LLM + context
4. Suggest remediation actions
5. Execute remediation (if approved)

Built on LangGraph for deterministic state management.
"""

from app.workflows.incident_response.state import IncidentState
from app.workflows.incident_response.graph import build_incident_workflow
from app.workflows.incident_response.router import route_incident

__all__ = [
    "IncidentState",
    "build_incident_workflow",
    "route_incident",
]

