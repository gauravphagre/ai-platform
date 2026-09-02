from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.infrastructure.database.base import Base

class Incident(Base):
    """Minimal incident persistence model (placeholder for future expansion)."""

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True)
    severity = Column(String)
    description = Column(Text)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

