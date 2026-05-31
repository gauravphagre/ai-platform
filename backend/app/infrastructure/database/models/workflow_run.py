from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, UTC

from app.infrastructure.database.database import Base


class WorkflowRun(Base):
    """Workflow run persistence.

    Stores workflow state as JSON for polling endpoints.
    """

    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, index=True)
    workflow_type = Column(String, index=True)
    status = Column(String, default="running")
    state = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
