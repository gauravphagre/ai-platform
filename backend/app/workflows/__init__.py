
"""
Workflows Module

LangGraph-based deterministic workflows for:
- Incident response automation
- Task orchestration
- Agent coordination
- State machine workflows

Architecture:
- All state is Pydantic-serializable
- Checkpoints enable pause/resume
- LLM integration via central LLMService
- Observable via structured logging

Usage:

from app.workflows.incident_response import build_incident_workflow, IncidentState

workflow = build_incident_workflow()
state = IncidentState(
    incident_id="INC-123",
    incident_description="High error rate detected",
    severity="high",
    created_at="2026-05-24T10:00:00Z",
    updated_at="2026-05-24T10:00:00Z",
)

# Run workflow
output = workflow.invoke(state)

# Or stream events
for event in workflow.stream(state):
    print(event)
"""

from app.workflows.incident_response import (
    IncidentState,
    build_incident_workflow,
    route_incident,
)
from app.workflows.common import (
    BaseWorkflowState,
    state_to_dict,
    dict_to_state,
    log_node_transition,
)

__all__ = [
    # Incident Response
    "IncidentState",
    "build_incident_workflow",
    "route_incident",
    # Common
    "BaseWorkflowState",
    "state_to_dict",
    "dict_to_state",
    "log_node_transition",
]

