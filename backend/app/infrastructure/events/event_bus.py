"""Event bus implementation.

In-memory event bus for publishing and subscribing to platform events.
In production, replace with external event broker (RabbitMQ, Kafka, AWS SNS/SQS).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any
import asyncio

from app.events.event_models import EventType


@dataclass
class EventBus:
    """In-memory event bus."""

    _subscribers: dict[str, list[Callable[[EventType], Any]]] = field(default_factory=dict)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    def subscribe(self, event_type: str, handler: Callable[[EventType], Any]) -> None:
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event: EventType) -> None:
        """Publish an event to all subscribers."""
        async with self._lock:
            handlers = self._subscribers.get(event.event_type, [])
            for handler in handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    # Log but don't fail the publish
                    print(f"Error in event handler: {e}")

    def unsubscribe(self, event_type: str, handler: Callable[[EventType], Any]) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                h for h in self._subscribers[event_type] if h != handler
            ]

