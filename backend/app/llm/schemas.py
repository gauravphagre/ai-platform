from typing import Literal, Optional, Any

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal[
        "system",
        "user",
        "assistant",
        "tool",
    ]

    content: str

    name: Optional[str] = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    """A tool invocation requested by the model."""

    id: Optional[str] = None
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """Result of executing a tool call."""

    tool_call_id: Optional[str] = None
    name: Optional[str] = None
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class GenerateRequest(BaseModel):
    messages: list[ChatMessage]

    model: str = "qwen2.5-coder:7b"

    temperature: float = 0.7

    max_tokens: Optional[int] = 2048

    stream: bool = False

    # Optional tool support (provider-dependent)
    tools: Optional[list[dict[str, Any]]] = None


class StreamToken(BaseModel):
    """A single streamed token/chunk from the provider."""

    content: str
    index: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class GenerateResponse(BaseModel):
    content: str

    model: str

    usage: Optional[dict[str, int]] = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    tool_calls: Optional[list[ToolCall]] = None


class BatchGenerateRequest(BaseModel):
    requests: list[GenerateRequest]


class BatchGenerateResponse(BaseModel):
    responses: list[GenerateResponse]


class EmbeddingRequest(BaseModel):
    text: str

    model: str = "nomic-embed-text"


class EmbeddingResponse(BaseModel):
    embedding: list[float]

    model: str


class TokenCountRequest(BaseModel):
    text: str
    model: Optional[str] = None


class TokenCountResponse(BaseModel):
    tokens: int
    model: Optional[str] = None


class ConversationContext(BaseModel):
    """Optional structured context that can be injected into prompts."""

    summary: Optional[str] = None
    facts: dict[str, Any] = Field(default_factory=dict)


class ChatCompletionRequest(BaseModel):
    """OpenAI-style request shape (useful as an adapter layer)."""

    messages: list[ChatMessage]
    model: str
    temperature: float = 0.7
    stream: bool = False
    max_tokens: Optional[int] = 2048


class LLMConfig(BaseModel):
    """Runtime configuration for selecting provider/model defaults."""

    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = 2048

