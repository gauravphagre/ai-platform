from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI database dependency.
    Creates and closes database session automatically.
    """
    async with AsyncSessionLocal() as session:
        yield session