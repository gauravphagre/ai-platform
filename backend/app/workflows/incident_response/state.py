"""
Incident Response Workflow State

Pydantic-based state model for incident workflow.
Serializable across LangGraph checkpoints.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    """Single log line from observability system."""
    timestamp: str
    level: str
    message: str
    service: str
    trace_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Metric(BaseModel):
    """Single metric from monitoring system."""
    name: str
    timestamp: str
    value: float
    unit: str
    labels: dict[str, str] = Field(default_factory=dict)


class RootCauseAnalysis(BaseModel):
    """Output of root cause analysis."""
    hypothesis: str
    confidence: float  # 0.0 - 1.0
    affected_services: list[str] = Field(default_factory=list)
    contributing_factors: list[str] = Field(default_factory=list)


class RemediationAction(BaseModel):
    """Suggested remediation."""
    action: str
    priority: int  # 1 (critical) to 5 (low)
    estimated_duration_seconds: int
    rollback_plan: Optional[str] = None
    prerequisites: list[str] = Field(default_factory=list)


class IncidentState(BaseModel):
    """
    State object for incident response workflow.

    Tracks incident context, collected data, analysis, and decisions.
    """

    # ==================== INPUT ====================
    incident_id: str
    incident_description: str
    severity: str  # "critical", "high", "medium", "low"

    # ==================== COLLECTED DATA ====================
    logs: list[LogEntry] = Field(default_factory=list)
    metrics: list[Metric] = Field(default_factory=list)

    # ==================== ANALYSIS ====================
    root_cause: Optional[RootCauseAnalysis] = None

    # ==================== REMEDIATION ====================
    remediation_actions: list[RemediationAction] = Field(default_factory=list)
    selected_action: Optional[RemediationAction] = None

    # ==================== EXECUTION ====================
    executed: bool = False
    execution_status: Optional[str] = None
    execution_error: Optional[str] = None

    # ==================== METADATA ====================
    created_at: str
    updated_at: str
    workflow_run_id: Optional[str] = None
    checkpoint: Optional[str] = None

