from fastapi import APIRouter, Depends, Query
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


@router.delete("/")
async def delete_conversations(
    all: bool = Query(False, description="Delete all conversations"),
    n: int | None = Query(None, ge=1, description="Delete most recent N conversations"),
    db: AsyncSession = Depends(get_db),
):
    if all:
        deleted = await conversation_service.delete_all_conversations(db)
        return {"deleted": deleted, "mode": "all"}

    if n is not None:
        deleted = await conversation_service.delete_recent_conversations(db, n)
        return {"deleted": deleted, "mode": "recent", "n": n}

    return {
        "deleted": 0,
        "error": "Specify either ?all=true or ?n=<number>",
    }
