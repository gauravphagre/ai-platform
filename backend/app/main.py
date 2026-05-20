import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from app.api.routes import rag
from prometheus_client import generate_latest

from app.routes.chat import router as chat_router
from app.observability.telemetry import setup_telemetry

from app.db.database import engine
from app.db.database import Base

from app.routes.conversations import router as conversations_router

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
    rag.router,
    prefix="/rag",
)

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