from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.llm.schemas import (
    ChatMessage,
    GenerateResponse,
    EmbeddingResponse
)


class BaseLLMProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        messages: list[ChatMessage],
        model: str,
        **kwargs
    ) -> GenerateResponse:
        pass

    @abstractmethod
    async def stream(
        self,
        messages: list[ChatMessage],
        model: str,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    async def embeddings(
        self,
        text: str,
        model: str
    ) -> EmbeddingResponse:
        pass