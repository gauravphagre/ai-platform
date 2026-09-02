"""
Incident Routing Logic

Determines how to route incidents based on:
- Severity
- Confidence of root cause
- Action priority
- Auto-remediation eligibility
"""

from app.workflows.incident_response.state import IncidentState, RemediationAction


def route_incident(state: IncidentState) -> str:
    """
    Route incident to appropriate handler.

    Routes:
    - "auto_execute": Auto-remediate (low severity + high confidence)
    - "human_review": Require human approval (high severity)
    - "quarantine": Isolate/alert (critical + unknown root cause)

    Args:
        state: Current incident state

    Returns:
        str: Route name ("auto_execute", "human_review", "quarantine")
    """

    if not state.root_cause:
        return "quarantine"

    # Quarantine if uncertain about root cause
    if state.root_cause.confidence < 0.5:
        return "quarantine"

    # Auto-execute for low-severity, high-confidence incidents
    if state.severity == "low" and state.root_cause.confidence >= 0.8:
        return "auto_execute"

    # Human review for medium/high/critical
    if state.severity in ("medium", "high", "critical"):
        return "human_review"

    return "human_review"


def should_auto_remediate(state: IncidentState) -> bool:
    """
    Determine if remediation should execute automatically.

    Criteria:
    - Root cause confidence >= 0.8
    - Severity is "low" or "medium"
    - Selected action has no prerequisites

    Args:
        state: Current incident state

    Returns:
        bool: True if auto-remediation is safe
    """

    if not state.root_cause or not state.selected_action:
        return False

    if state.root_cause.confidence < 0.8:
        return False

    if state.severity not in ("low", "medium"):
        return False

    if state.selected_action.prerequisites:
        return False

    return True

