import logging

from contextlib import asynccontextmanager
from app.api.health.health import router as health_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from app.api.rag.rag import router as rag
from prometheus_client import generate_latest

from app.api.chat.chat import router as chat_router
from app.api.workflows.workflows import router as workflows_router
from app.observability.telemetry import setup_telemetry

from app.infrastructure.database.database import engine
from app.infrastructure.database.base import Base

from app.api.conversations.conversations import router as conversations_router
from app.infrastructure.database.models import (
    Conversation,
    Message,
)


# Configure logger
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("ai-backend")


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting application...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    setup_telemetry(app)

    yield

    logger.info("Shutting down application...")


app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

app.include_router(conversations_router)

app.include_router(
    rag,
    prefix="/rag",
)

app.include_router(workflows_router)

app.include_router(health_router)

@app.get("/")
def home():
    logger.info("Health check endpoint called.")
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    logger.debug("Metrics endpoint scraped.")
    return Response(
        generate_latest(),
        media_type="text/plain"
    )