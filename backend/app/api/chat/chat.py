import json
import time

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.ext.asyncio import AsyncSession

from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

from app.core.dependencies import get_db
from app.core.settings import settings

from app.schemas.chat import ChatRequest, ChatResponse

from app.llm.service import LLMService

from app.llm.schemas import (
    ChatMessage as LLMChatMessage,
    GenerateRequest,
)

from app.api.chat.utils import build_chat_messages

from app.observability.metrics import count_tokens
from app.observability.logger import log_event

from app.services.conversation_service import ConversationService

router = APIRouter()

llm_service = LLMService()
conversation_service = ConversationService()

tracer = trace.get_tracer("chat-service")


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):

    start_time = time.time()

    with tracer.start_as_current_span("chat-request") as span:

        span.set_attribute(
            "model",
            request.model or settings.DEFAULT_MODEL
        )

        span.set_attribute(
            "message_count",
            len(request.messages)
        )

        # =========================================
        # Conversation Handling
        # =========================================

        with tracer.start_as_current_span(
            "db.create_conversation"
        ):

            if request.conversation_id:
                conversation_id = request.conversation_id

            else:
                conversation = (
                    await conversation_service
                    .create_conversation(db)
                )

                conversation_id = conversation.id

        latest_message = request.messages[-1]

        with tracer.start_as_current_span(
            "db.insert_user_message"
        ):

            await conversation_service.add_message(
                db,
                conversation_id,
                latest_message.role,
                latest_message.content,
            )

        span.set_attribute(
            "conversation_id",
            str(conversation_id)
        )

        # =========================================
        # Logging
        # =========================================

        log_event(
            "request_received",
            {
                "messages": [
                    m.model_dump()
                    for m in request.messages
                ],
                "model": (
                    request.model
                    or settings.DEFAULT_MODEL
                ),
            },
        )

        # =========================================
        # Fetch Full Conversation History
        # =========================================

        try:

            with tracer.start_as_current_span(
                "db.fetch_conversation_history"
            ):

                history = (
                    await conversation_service
                    .get_messages(
                        db,
                        conversation_id
                    )
                )

            # =========================================
            # Build LLM Messages
            # =========================================

            llm_messages: list[LLMChatMessage] = (
                build_chat_messages(history)
            )

            llm_request = GenerateRequest(
                messages=llm_messages,
                model=(
                    request.model
                    or settings.DEFAULT_MODEL
                ),
                stream=False,
            )

            # =========================================
            # LLM Generation
            # =========================================

            with tracer.start_as_current_span(
                "llm.generate_response"
            ):

                llm_response = (
                    await llm_service
                    .generate_response(
                        llm_request
                    )
                )

                response_text = llm_response.content

        except Exception as e:

            span.record_exception(e)

            span.set_status(
                Status(StatusCode.ERROR)
            )

            log_event(
                "llm_error",
                {
                    "error": str(e)
                }
            )

            response_text = (
                "LLM error occurred. "
                "Please try again."
            )

        # =========================================
        # Metrics
        # =========================================

        latency = time.time() - start_time

        with tracer.start_as_current_span(
            "metrics.compute_tokens"
        ):

            tokens = count_tokens(response_text)

        # =========================================
        # Store Assistant Response
        # =========================================

        with tracer.start_as_current_span(
            "db.insert_assistant_message"
        ):

            await conversation_service.add_message(
                db,
                conversation_id,
                "assistant",
                response_text,
            )

        # =========================================
        # Final Span Enrichment
        # =========================================

        span.set_attribute(
            "latency",
            latency
        )

        span.set_attribute(
            "tokens",
            tokens
        )

        log_event(
            "response_sent",
            {
                "latency": latency,
                "tokens": tokens,
            },
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            latency=latency,
            tokens=tokens,
            model=(
                request.model
                or settings.DEFAULT_MODEL
            ),
        )


@router.post("/chat/stream")
async def stream_chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):

    # =========================================
    # Conversation Handling
    # =========================================

    if request.conversation_id:

        conversation_id = request.conversation_id

    else:

        conversation = (
            await conversation_service
            .create_conversation(db)
        )

        conversation_id = conversation.id

    latest_message = request.messages[-1]

    await conversation_service.add_message(
        db,
        conversation_id,
        latest_message.role,
        latest_message.content,
    )

    # =========================================
    # Fetch Conversation History
    # =========================================

    history = await conversation_service.get_messages(
        db,
        conversation_id
    )

    llm_messages: list[LLMChatMessage] = (
        build_chat_messages(history)
    )

    llm_request = GenerateRequest(
        messages=llm_messages,
        model=(
            request.model
            or settings.DEFAULT_MODEL
        ),
        stream=True,
    )

    # =========================================
    # SSE Event Generator
    # =========================================

    async def event_generator():

        chunks = []

        async for chunk in llm_service.stream_response(
            llm_request
        ):

            chunks.append(chunk)

            yield (
                f"data: "
                f"{json.dumps({'token': chunk})}\n\n"
            )

        full_response = "".join(chunks)

        # =========================================
        # Save Assistant Response
        # =========================================

        await conversation_service.add_message(
            db,
            conversation_id,
            "assistant",
            full_response,
        )

        yield (
            f"data: "
            f"{json.dumps({'done': True})}\n\n"
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )