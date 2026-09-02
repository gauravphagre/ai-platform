from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Conversation, Message


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str | None = None) -> Conversation:
        conversation = Conversation(title=title)

        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        return conversation

    async def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )


        return result.scalar_one_or_none()

    async def list_all(self) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation)
        )

        return list(result.scalars().all())

    async def get_all_conversations(self) -> list[Conversation]:
        """Backward-compatible alias for older code paths."""
        return await self.list_all()

    async def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
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
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )

        return list(result.scalars().all())

    async def delete(
        self,
        conversation: Conversation,
    ) -> None:
        await self.db.delete(conversation)
        await self.db.commit()

    async def update_title(
        self,
        conversation_id: int,
        title: str,
    ) -> Conversation | None:
        conversation = await self.get_by_id(conversation_id)
        if not conversation:
            return None

        conversation.title = title
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def list_recent(self, limit: int) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete_all(self) -> int:
        conversations = await self.list_all()
        for c in conversations:
            await self.db.delete(c)
        await self.db.commit()
        return len(conversations)

    async def delete_recent(self, limit: int) -> int:
        conversations = await self.list_recent(limit)
        for c in conversations:
            await self.db.delete(c)
        await self.db.commit()
        return len(conversations)
