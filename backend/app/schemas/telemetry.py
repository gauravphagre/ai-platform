"""Telemetry schemas."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime


class TelemetrySpan(BaseModel):
    trace_id: str
    span_id: str
    name: str
    start_time: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    end_time: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class TelemetryMetric(BaseModel):
    name: str
    value: float
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    labels: dict[str, str] = Field(default_factory=dict)

