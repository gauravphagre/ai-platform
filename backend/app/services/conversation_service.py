from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    async def create_conversation(self, db: AsyncSession):
        return await ConversationRepository(db).create()

    async def add_message(self, db: AsyncSession, conversation_id, role, content):
        return await ConversationRepository(db).add_message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

    async def get_messages(self, db: AsyncSession, conversation_id: int):
        return await ConversationRepository(db).get_messages(conversation_id)

    async def get_all_conversations(self, db: AsyncSession):
        conversations = await ConversationRepository(db).list_all()
        return [
            {
                "id": c.id,
                "title": c.title,
                "created_at": (
                    c.created_at.isoformat()
                    if getattr(c, "created_at", None)
                    else None
                ),
            }
            for c in conversations
        ]

    async def get_conversation_messages(self, db: AsyncSession, conversation_id: int):
        messages = await ConversationRepository(db).get_messages(conversation_id)
        return [
            {"role": m.role, "content": m.content, "created_at": m.created_at}
            for m in messages
        ]

    async def set_title(
        self,
        db: AsyncSession,
        conversation_id: int,
        title: str,
    ):
        return await ConversationRepository(db).update_title(
            conversation_id=conversation_id,
            title=title,
        )

    async def delete_all_conversations(self, db: AsyncSession) -> int:
        return await ConversationRepository(db).delete_all()

    async def delete_recent_conversations(self, db: AsyncSession, limit: int) -> int:
        return await ConversationRepository(db).delete_recent(limit)
