import time

from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.llm.inference import LLMInferenceService
from app.observability.metrics import count_tokens
from app.observability.logger import log_event
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.services.conversation_service import ConversationService

router = APIRouter()
llm_service = LLMInferenceService()
conversation_service = ConversationService()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()

    if request.conversation_id:
        conversation_id = request.conversation_id
    else:
        conversation = await conversation_service.create_conversation(db)
        conversation_id = conversation.id

    latest_message = request.messages[-1]

    await conversation_service.add_message(
        db,
        conversation_id,
        latest_message.role,
        latest_message.content
    )

    log_event(
        "request_received",
        {
            "messages": [m.dict() for m in request.messages],
            "model": request.model
        }
    )
    try:
        response_text = llm_service.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI inside ai-platform."
                },
                *[m.dict() for m in request.messages]
            ],
            model=request.model,
            stream=request.stream
        )

    except Exception as e:
        log_event("llm_error", {"error": str(e)})
        response_text = "LLM error occurred. Please try again."

    latency = time.time() - start_time

    tokens = count_tokens(response_text)

    await conversation_service.add_message(
        db,
        conversation_id,
        "assistant",
        response_text
    )

    log_event(
        "response_sent",
        {
            "latency": latency,
            "tokens": tokens
        }
    )

    return ChatResponse(
        response=response_text,
        latency=latency,
        tokens=tokens,
        model=request.model
    )