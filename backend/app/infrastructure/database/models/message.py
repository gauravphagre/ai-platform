from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.infrastructure.database.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )

