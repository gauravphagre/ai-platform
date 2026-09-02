"""
Incident Response Workflow Graph

LangGraph-based workflow implementation.

Nodes:
- retrieve_logs: Fetch logs from observability
- retrieve_metrics: Fetch metrics from monitoring
- analyze_root_cause: LLM-powered analysis
- suggest_remediation: LLM-powered recommendations
- route_decision: Route to execution or human review
"""

from typing import Any, Callable
from langgraph.graph import StateGraph, END
from app.workflows.incident_response.state import IncidentState
from app.workflows.incident_response.nodes import (
    retrieve_logs,
    retrieve_metrics,
    analyze_root_cause,
    suggest_remediation,
)


def build_incident_workflow() -> StateGraph:
    """
    Construct the incident response workflow graph.

    Returns:
        StateGraph: Compiled LangGraph workflow
    """

    workflow = StateGraph(IncidentState)

    # ==================== ADD NODES ====================
    workflow.add_node("retrieve_logs", retrieve_logs)
    workflow.add_node("retrieve_metrics", retrieve_metrics)
    workflow.add_node("analyze_root_cause", analyze_root_cause)
    workflow.add_node("suggest_remediation", suggest_remediation)

    # ==================== ADD EDGES ====================
    # Start -> retrieve logs and metrics in parallel
    workflow.add_edge("START", "retrieve_logs")
    workflow.add_edge("START", "retrieve_metrics")

    # After both data collection steps, move to analysis
    workflow.add_edge("retrieve_logs", "analyze_root_cause")
    workflow.add_edge("retrieve_metrics", "analyze_root_cause")

    # After analysis, suggest remediation
    workflow.add_edge("analyze_root_cause", "suggest_remediation")

    # After remediation suggestions, end (human can pick one)
    workflow.add_edge("suggest_remediation", END)

    # ==================== SET ENTRY ====================
    workflow.set_entry_point("retrieve_logs")

    return workflow.compile()


def build_incident_workflow_with_execution() -> StateGraph:
    """
    Extended workflow that includes automatic remediation execution
    for low-severity incidents.

    Returns:
        StateGraph: Compiled workflow with execution node
    """

    workflow = build_incident_workflow()
    # TODO: Add execute_remediation node with conditional routing
    return workflow

