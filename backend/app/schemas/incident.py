"""Incident domain schemas."""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Incident(BaseModel):
    incident_id: str
    severity: str
    description: str
    status: str = "open"  # open, investigating, mitigated, resolved
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    root_cause: Optional[str] = None
    confidence: Optional[float] = None

