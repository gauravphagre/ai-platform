from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    messages: List[ChatMessage]
    model: Optional[str] = "qwen2.5-coder:7b"
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    latency: float
    tokens: int
    model: str