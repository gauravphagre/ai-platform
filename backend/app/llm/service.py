from typing import AsyncGenerator

from app.llm.providers.ollama_provider import OllamaProvider

from app.llm.schemas import (
    GenerateRequest,
    GenerateResponse,
    EmbeddingResponse,
)


class LLMService:

    def __init__(self):
        self.provider = OllamaProvider()

    async def generate_response(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:

        return await self.provider.generate(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

    async def stream_response(
        self,
        request: GenerateRequest,
    ) -> AsyncGenerator[str, None]:

        async for token in self.provider.stream(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        ):
            yield token

    async def generate_embeddings(
        self,
        text: str,
        model: str = "nomic-embed-text",
    ) -> EmbeddingResponse:

        return await self.provider.embeddings(
            text=text,
            model=model,
        )