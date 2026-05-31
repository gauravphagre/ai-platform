"""Conversation repository."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Conversation, Message


@dataclass
class ConversationRepository:
    db: AsyncSession

    async def create_conversation(self) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation()
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def add_message(self, conversation_id: int, role: str, content: str) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages(self, conversation_id: int) -> list[Message]:
        """Get all messages for a conversation."""
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_all_conversations(self) -> list[Conversation]:
        """Get all conversations."""
        result = await self.db.execute(
            select(Conversation).order_by(Conversation.created_at.desc())
        )
        return list(result.scalars().all())
