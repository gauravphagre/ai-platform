"""Event publishers.

Helper functions for publishing events to the event bus.
Makes it easy for workflow nodes and services to emit events.
"""

from __future__ import annotations

from typing import Optional, Any

from app.events.event_models import (
    LLMGenerateStarted,
    LLMGenerateCompleted,
    LLMGenerateFailed,
    LLMStreamStarted,
    LLMStreamToken,
    LLMStreamCompleted,
    WorkflowStarted,
    WorkflowCompleted,
    WorkflowFailed,
    WorkflowNodeStarted,
    WorkflowNodeCompleted,
    IncidentCreated,
    IncidentAnalyzed,
    IncidentResolved,
    ToolCalled,
    ToolCompleted,
    ToolFailed,
    RAGRetrievalStarted,
    RAGRetrievalCompleted,
)


class LLMEventPublisher:
    """Publish LLM-related events."""

    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def publish_generate_started(self, model: str, message_count: int):
        await self.event_bus.publish(
            LLMGenerateStarted(source="llm", model=model, message_count=message_count)
        )

    async def publish_generate_completed(
        self, model: str, tokens_used: int, latency_ms: float
    ):
        await self.event_bus.publish(
            LLMGenerateCompleted(
                source="llm", model=model, tokens_used=tokens_used, latency_ms=latency_ms
            )
        )

    async def publish_generate_failed(self, model: str, error: str):
        await self.event_bus.publish(
            LLMGenerateFailed(source="llm", model=model, error=error)
        )

    async def publish_stream_started(self, model: str):
        await self.event_bus.publish(LLMStreamStarted(source="llm", model=model))

    async def publish_stream_token(self, model: str, token: str):
        await self.event_bus.publish(
            LLMStreamToken(source="llm", model=model, token=token)
        )

    async def publish_stream_completed(self, model: str, total_tokens: int):
        await self.event_bus.publish(
            LLMStreamCompleted(source="llm", model=model, total_tokens=total_tokens)
        )


class WorkflowEventPublisher:
    """Publish workflow-related events."""

    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def publish_started(
        self, workflow_id: str, workflow_type: str, input_size: int
    ):
        await self.event_bus.publish(
            WorkflowStarted(
                source="workflows",
                workflow_id=workflow_id,
                workflow_type=workflow_type,
                input_size=input_size,
            )
        )

    async def publish_completed(
        self, workflow_id: str, workflow_type: str, latency_ms: float, status: str
    ):
        await self.event_bus.publish(
            WorkflowCompleted(
                source="workflows",
                workflow_id=workflow_id,
                workflow_type=workflow_type,
                latency_ms=latency_ms,
                status=status,
            )
        )

    async def publish_failed(self, workflow_id: str, workflow_type: str, error: str):
        await self.event_bus.publish(
            WorkflowFailed(
                source="workflows",
                workflow_id=workflow_id,
                workflow_type=workflow_type,
                error=error,
            )
        )

    async def publish_node_started(self, workflow_id: str, node_name: str):
        await self.event_bus.publish(
            WorkflowNodeStarted(
                source="workflows", workflow_id=workflow_id, node_name=node_name
            )
        )

    async def publish_node_completed(
        self, workflow_id: str, node_name: str, latency_ms: float
    ):
        await self.event_bus.publish(
            WorkflowNodeCompleted(
                source="workflows",
                workflow_id=workflow_id,
                node_name=node_name,
                latency_ms=latency_ms,
            )
        )


class IncidentEventPublisher:
    """Publish incident-related events."""

    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def publish_created(self, incident_id: str, severity: str, description: str):
        await self.event_bus.publish(
            IncidentCreated(
                source="workflows",
                incident_id=incident_id,
                severity=severity,
                description=description,
            )
        )

    async def publish_analyzed(self, incident_id: str, root_cause_confidence: float):
        await self.event_bus.publish(
            IncidentAnalyzed(
                source="workflows",
                incident_id=incident_id,
                root_cause_confidence=root_cause_confidence,
            )
        )

    async def publish_resolved(self, incident_id: str, resolution: str):
        await self.event_bus.publish(
            IncidentResolved(
                source="workflows", incident_id=incident_id, resolution=resolution
            )
        )


class ToolEventPublisher:
    """Publish tool-related events."""

    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def publish_called(self, tool_name: str, tool_input: dict[str, Any]):
        await self.event_bus.publish(
            ToolCalled(source="tools", tool_name=tool_name, tool_input=tool_input)
        )

    async def publish_completed(self, tool_name: str, latency_ms: float, output_size: int):
        await self.event_bus.publish(
            ToolCompleted(
                source="tools",
                tool_name=tool_name,
                latency_ms=latency_ms,
                output_size=output_size,
            )
        )

    async def publish_failed(self, tool_name: str, error: str):
        await self.event_bus.publish(
            ToolFailed(source="tools", tool_name=tool_name, error=error)
        )


class RAGEventPublisher:
    """Publish RAG-related events."""

    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def publish_retrieval_started(self, query: str):
        await self.event_bus.publish(
            RAGRetrievalStarted(source="rag", query=query)
        )

    async def publish_retrieval_completed(self, chunks_retrieved: int, latency_ms: float):
        await self.event_bus.publish(
            RAGRetrievalCompleted(
                source="rag",
                chunks_retrieved=chunks_retrieved,
                latency_ms=latency_ms,
            )
        )

