"""Event models for the platform.

Pydantic models for all event types published across the platform:
- LLM events (generate, stream, error)
- Workflow events (start, complete, fail)
- Incident events (created, resolved)
- Tool events (called, failed)
"""

from __future__ import annotations

from typing import Any, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Event(BaseModel):
    """Base event model."""

    event_type: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    event_id: str = Field(default_factory=lambda: str(__import__("uuid").uuid4()))
    source: str  # Which component emitted this (e.g., "llm", "workflows", "rag")
    metadata: dict[str, Any] = Field(default_factory=dict)


# ==================== LLM EVENTS ====================


class LLMGenerateStarted(Event):
    """LLM generation started."""

    event_type: Literal["llm.generate.started"] = "llm.generate.started"
    model: str
    message_count: int


class LLMGenerateCompleted(Event):
    """LLM generation completed."""

    event_type: Literal["llm.generate.completed"] = "llm.generate.completed"
    model: str
    tokens_used: int
    latency_ms: float


class LLMGenerateFailed(Event):
    """LLM generation failed."""

    event_type: Literal["llm.generate.failed"] = "llm.generate.failed"
    model: str
    error: str


class LLMStreamStarted(Event):
    """LLM streaming started."""

    event_type: Literal["llm.stream.started"] = "llm.stream.started"
    model: str


class LLMStreamToken(Event):
    """LLM stream token received."""

    event_type: Literal["llm.stream.token"] = "llm.stream.token"
    model: str
    token: str


class LLMStreamCompleted(Event):
    """LLM streaming completed."""

    event_type: Literal["llm.stream.completed"] = "llm.stream.completed"
    model: str
    total_tokens: int


# ==================== WORKFLOW EVENTS ====================


class WorkflowStarted(Event):
    """Workflow execution started."""

    event_type: Literal["workflow.started"] = "workflow.started"
    workflow_id: str
    workflow_type: str
    input_size: int


class WorkflowCompleted(Event):
    """Workflow execution completed."""

    event_type: Literal["workflow.completed"] = "workflow.completed"
    workflow_id: str
    workflow_type: str
    latency_ms: float
    status: str


class WorkflowFailed(Event):
    """Workflow execution failed."""

    event_type: Literal["workflow.failed"] = "workflow.failed"
    workflow_id: str
    workflow_type: str
    error: str


class WorkflowNodeStarted(Event):
    """Workflow node started."""

    event_type: Literal["workflow.node.started"] = "workflow.node.started"
    workflow_id: str
    node_name: str


class WorkflowNodeCompleted(Event):
    """Workflow node completed."""

    event_type: Literal["workflow.node.completed"] = "workflow.node.completed"
    workflow_id: str
    node_name: str
    latency_ms: float


# ==================== INCIDENT EVENTS ====================


class IncidentCreated(Event):
    """Incident created."""

    event_type: Literal["incident.created"] = "incident.created"
    incident_id: str
    severity: str
    description: str


class IncidentAnalyzed(Event):
    """Incident analyzed."""

    event_type: Literal["incident.analyzed"] = "incident.analyzed"
    incident_id: str
    root_cause_confidence: float


class IncidentResolved(Event):
    """Incident resolved."""

    event_type: Literal["incident.resolved"] = "incident.resolved"
    incident_id: str
    resolution: str


# ==================== TOOL EVENTS ====================


class ToolCalled(Event):
    """Tool was called."""

    event_type: Literal["tool.called"] = "tool.called"
    tool_name: str
    tool_input: dict[str, Any]


class ToolCompleted(Event):
    """Tool execution completed."""

    event_type: Literal["tool.completed"] = "tool.completed"
    tool_name: str
    latency_ms: float
    output_size: int


class ToolFailed(Event):
    """Tool execution failed."""

    event_type: Literal["tool.failed"] = "tool.failed"
    tool_name: str
    error: str


# ==================== RAG EVENTS ====================


class RAGRetrievalStarted(Event):
    """RAG retrieval started."""

    event_type: Literal["rag.retrieval.started"] = "rag.retrieval.started"
    query: str


class RAGRetrievalCompleted(Event):
    """RAG retrieval completed."""

    event_type: Literal["rag.retrieval.completed"] = "rag.retrieval.completed"
    chunks_retrieved: int
    latency_ms: float


# Union of all event types
EventType = (
    LLMGenerateStarted
    | LLMGenerateCompleted
    | LLMGenerateFailed
    | LLMStreamStarted
    | LLMStreamToken
    | LLMStreamCompleted
    | WorkflowStarted
    | WorkflowCompleted
    | WorkflowFailed
    | WorkflowNodeStarted
    | WorkflowNodeCompleted
    | IncidentCreated
    | IncidentAnalyzed
    | IncidentResolved
    | ToolCalled
    | ToolCompleted
    | ToolFailed
    | RAGRetrievalStarted
    | RAGRetrievalCompleted
)

