import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from opentelemetry import trace

from app.models.chat import ChatRequest, ChatResponse
from app.llm.inference import LLMInferenceService
from app.observability.metrics import count_tokens
from app.observability.logger import log_event
from app.core.dependencies import get_db
from app.services.conversation_service import ConversationService


router = APIRouter()

llm_service = LLMInferenceService()
conversation_service = ConversationService()

# SINGLE tracer instance (correct way)
tracer = trace.get_tracer("chat-service")


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):

    start_time = time.time()

    # 🔥 MAIN FIX: CREATE REAL OTEL SPAN
    print("SPAN STARTING")
    with tracer.start_as_current_span("chat-request") as span:
        print("SPAN ACTIVE")

        span.set_attribute("model", request.model)
        span.set_attribute("message_count", len(request.messages))

        # ---------------------------
        # Conversation handling
        # ---------------------------
        with tracer.start_as_current_span("db.create_conversation"):

            if request.conversation_id:
                conversation_id = request.conversation_id
            else:
                conversation = await conversation_service.create_conversation(db)
                conversation_id = conversation.id

        latest_message = request.messages[-1]

        with tracer.start_as_current_span("db.insert_user_message"):

            await conversation_service.add_message(
                db,
                conversation_id,
                latest_message.role,
                latest_message.content
            )

        span.set_attribute("conversation_id", str(conversation_id))

        # ---------------------------
        # Logging
        # ---------------------------
        log_event(
            "request_received",
            {
                "messages": [m.dict() for m in request.messages],
                "model": request.model
            }
        )

        # ---------------------------
        # LLM CALL
        # ---------------------------
        try:
            with tracer.start_as_current_span("llm.generate_response"):
                # ---------------------------
                # BUILD FULL CONVERSATION CONTEXT
                # ---------------------------

                with tracer.start_as_current_span("db.fetch_conversation_history"):
                    history = await conversation_service.get_messages(
                        db,
                        conversation_id
                    )
                    print("HISTORY:")
                    for msg in history:
                        print(msg.role, "=>", msg.content)

                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI inside ai-platform."
                    }
                ]

                # Add historical messages
                messages.extend([
                    {
                        "role": msg.role,
                        "content": msg.content
                    }
                    for msg in history
                ])

                # ---------------------------
                # LLM CALL
                # ---------------------------

                with tracer.start_as_current_span("llm.generate_response"):
                    response_text = llm_service.generate_response(
                        messages=messages,
                        model=request.model,
                        stream=request.stream
                    )

        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR))

            log_event("llm_error", {"error": str(e)})
            response_text = "LLM error occurred. Please try again."

        # ---------------------------
        # Metrics + DB
        # ---------------------------
        latency = time.time() - start_time
        with tracer.start_as_current_span("metrics.compute_tokens"):
            tokens = count_tokens(response_text)

        with tracer.start_as_current_span("db.insert_assistant_message"):
            await conversation_service.add_message(
                db,
                conversation_id,
                "assistant",
                response_text
            )

        # ---------------------------
        # Final logs + span enrichment
        # ---------------------------
        span.set_attribute("latency", latency)
        span.set_attribute("tokens", tokens)

        log_event(
            "response_sent",
            {
                "latency": latency,
                "tokens": tokens
            }
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            latency=latency,
            tokens=tokens,
            model=request.model
        )