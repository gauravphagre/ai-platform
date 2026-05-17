from sqlalchemy import select

from app.db.models import Conversation
from app.db.models import Message


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
        db,
        conversation_id
    ):

        result = await db.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at)
        )

        return result.scalars().all()