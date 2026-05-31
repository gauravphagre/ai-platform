"""Event system package.

In-memory event bus for publishing platform events (LLM, workflows, incidents, tools, RAG).

Usage:

from app.events.event_bus import EventBus
from app.events.publishers import LLMEventPublisher

event_bus = EventBus()
llm_pub = LLMEventPublisher(event_bus)

# Subscribe to events
async def on_llm_complete(event):
    print(f"LLM used {event.tokens_used} tokens")

event_bus.subscribe("llm.generate.completed", on_llm_complete)

# Publish events
await llm_pub.publish_generate_completed(model="qwen", tokens_used=150, latency_ms=1234)
"""

from app.events.event_bus import EventBus
from app.events.event_models import (
    Event,
    LLMGenerateStarted,
    LLMGenerateCompleted,
    LLMGenerateFailed,
    WorkflowStarted,
    WorkflowCompleted,
    IncidentCreated,
    ToolCalled,
    RAGRetrievalStarted,
)
from app.events.publishers import (
    LLMEventPublisher,
    WorkflowEventPublisher,
    IncidentEventPublisher,
    ToolEventPublisher,
    RAGEventPublisher,
)

__all__ = [
    # Event Bus
    "EventBus",
    # Event Models
    "Event",
    "LLMGenerateStarted",
    "LLMGenerateCompleted",
    "LLMGenerateFailed",
    "WorkflowStarted",
    "WorkflowCompleted",
    "IncidentCreated",
    "ToolCalled",
    "RAGRetrievalStarted",
    # Publishers
    "LLMEventPublisher",
    "WorkflowEventPublisher",
    "IncidentEventPublisher",
    "ToolEventPublisher",
    "RAGEventPublisher",
]

