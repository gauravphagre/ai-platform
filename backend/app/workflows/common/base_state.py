"""
Base Workflow State

Abstract base class for all workflow states.

Provides:
- Serialization/deserialization for LangGraph checkpointing
- Metadata tracking (created_at, updated_at, workflow_run_id)
- Status and error handling
"""

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class BaseWorkflowState(BaseModel):
    """
    Abstract base for all workflow states.

    Attributes:
        workflow_type: Name of workflow (e.g., "incident_response")
        workflow_run_id: Unique ID for this workflow run
        created_at: ISO timestamp when workflow started
        updated_at: ISO timestamp of last update
        checkpoint: Current node name
        status: Overall workflow status (running, completed, failed)
        error: Error message if failed
        metadata: Arbitrary workflow-specific data
    """

    workflow_type: str
    workflow_run_id: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    checkpoint: Optional[str] = None
    status: str = "running"  # running, completed, failed, paused
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Allow arbitrary types for extensibility."""
        arbitrary_types_allowed = True

    def mark_complete(self):
        """Mark workflow as successfully completed."""
        self.status = "completed"
        self.updated_at = datetime.utcnow().isoformat()

    def mark_failed(self, error: str):
        """Mark workflow as failed with error message."""
        self.status = "failed"
        self.error = error
        self.updated_at = datetime.utcnow().isoformat()

    def mark_paused(self):
        """Mark workflow as paused (e.g., waiting for human approval)."""
        self.status = "paused"
        self.updated_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state to dictionary (for checkpointing)."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseWorkflowState":
        """Deserialize state from dictionary (from checkpoint)."""
        return cls(**data)

