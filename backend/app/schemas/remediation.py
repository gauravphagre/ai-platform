"""Remediation schemas."""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RemediationAction(BaseModel):
    action_id: str
    incident_id: str
    action: str
    priority: int = 3
    status: str = "proposed"  # proposed, approved, executing, completed, failed
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    rollback_plan: Optional[str] = None
    error: Optional[str] = None

