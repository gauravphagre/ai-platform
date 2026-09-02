"""Workflow domain schemas."""

from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class WorkflowRun(BaseModel):
    workflow_id: str
    workflow_type: str
    status: str = "running"  # running, completed, failed, paused
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    checkpoint: Optional[str] = None
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

