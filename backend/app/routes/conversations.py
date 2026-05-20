from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations")

conversation_service = ConversationService()


@router.get("/")
async def get_conversations(
    db: AsyncSession = Depends(get_db)
):
    return await conversation_service.get_all_conversations(db)


@router.get("/{conversation_id}")
async def get_conversation_messages(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await conversation_service.get_conversation_messages(
        db,
        conversation_id
    )