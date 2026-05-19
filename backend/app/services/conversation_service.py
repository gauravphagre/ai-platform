from sqlalchemy import select

from app.db.models import Conversation
from app.db.models import Message
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.db.models import Conversation, Message


class ConversationService:

    async def create_conversation(
        self,
        db
    ):
        conversation = Conversation()
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation

    async def add_message(
        self,
        db,
        conversation_id,
        role,
        content
    ):
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(message)
        await db.commit()
        return message

    async def get_messages(
        self,
        db: AsyncSession,
        conversation_id: int
    ):
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )

        return result.scalars().all()

    async def get_all_conversations(
            self,
            db: AsyncSession
    ):
        result = await db.execute(
            select(Conversation).order_by(
                Conversation.created_at.desc()
            )
        )

        conversations = result.scalars().all()

        return [
            {
                "id": c.id,
                "created_at": c.created_at
            }
            for c in conversations
        ]

    async def get_conversation_messages(
            self,
            db: AsyncSession,
            conversation_id: int
    ):
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )

        messages = result.scalars().all()

        return [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            }
            for m in messages
        ]