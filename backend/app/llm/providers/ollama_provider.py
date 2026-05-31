import json

from typing import AsyncGenerator

import httpx

from app.core.settings import settings

from app.llm.interfaces import BaseLLMProvider

from app.llm.schemas import (
    ChatMessage,
    GenerateResponse,
    EmbeddingResponse,
)

from app.llm.exceptions import (
    LLMConnectionError,
    LLMProviderError,
)


DEFAULT_TIMEOUT = 300.0


class OllamaProvider(BaseLLMProvider):

    def __init__(self):

        self.base_url = settings.OLLAMA_BASE_URL

    # =========================================================
    # TEXT GENERATION
    # =========================================================

    async def generate(
        self,
        messages: list[ChatMessage],
        model: str,
        **kwargs,
    ) -> GenerateResponse:

        payload = {
            "model": model,
            "messages": [
                message.model_dump()
                for message in messages
            ],
            "stream": False,
            "options": {
                "temperature": kwargs.get(
                    "temperature",
                    0.7,
                ),
                "num_predict": kwargs.get(
                    "max_tokens",
                    1024,
                ),
            },
        }

        try:

            async with httpx.AsyncClient(
                timeout=DEFAULT_TIMEOUT
            ) as client:

                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

                message = data.get(
                    "message",
                    {}
                )

                return GenerateResponse(
                    content=message.get(
                        "content",
                        "",
                    ),
                    model=model,
                    metadata={
                        "done": data.get("done"),
                        "total_duration": data.get(
                            "total_duration"
                        ),
                        "load_duration": data.get(
                            "load_duration"
                        ),
                        "prompt_eval_count": data.get(
                            "prompt_eval_count"
                        ),
                        "eval_count": data.get(
                            "eval_count"
                        ),
                    },
                )

        except httpx.ConnectError as e:

            raise LLMConnectionError(
                f"Ollama connection failed: {str(e)}"
            )

        except httpx.HTTPStatusError as e:

            raise LLMProviderError(
                f"Ollama HTTP error: "
                f"{e.response.status_code}"
            )

        except Exception as e:

            raise LLMProviderError(
                f"Ollama generation failed: {str(e)}"
            )

    # =========================================================
    # STREAMING GENERATION
    # =========================================================

    async def stream(
        self,
        messages: list[ChatMessage],
        model: str,
        **kwargs,
    ) -> AsyncGenerator[str, None]:

        payload = {
            "model": model,
            "messages": [
                message.model_dump()
                for message in messages
            ],
            "stream": True,
            "options": {
                "temperature": kwargs.get(
                    "temperature",
                    0.7,
                ),
                "num_predict": kwargs.get(
                    "max_tokens",
                    1024,
                ),
            },
        }

        try:

            async with httpx.AsyncClient(
                timeout=None
            ) as client:

                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=payload,
                ) as response:

                    response.raise_for_status()

                    async for line in response.aiter_lines():

                        if not line:
                            continue

                        try:

                            data = json.loads(line)

                            message = data.get(
                                "message",
                                {}
                            )

                            token = message.get(
                                "content",
                                ""
                            )

                            if token:
                                yield token

                        except json.JSONDecodeError:
                            continue

        except httpx.ConnectError as e:

            raise LLMConnectionError(
                f"Ollama stream connection failed: "
                f"{str(e)}"
            )

        except httpx.HTTPStatusError as e:

            raise LLMProviderError(
                f"Ollama stream HTTP error: "
                f"{e.response.status_code}"
            )

        except Exception as e:

            raise LLMProviderError(
                f"Ollama stream failed: {str(e)}"
            )

    # =========================================================
    # EMBEDDINGS
    # =========================================================

    async def embeddings(
        self,
        text: str,
        model: str,
    ) -> EmbeddingResponse:

        payload = {
            "model": model,
            "prompt": text,
        }

        try:

            async with httpx.AsyncClient(
                timeout=DEFAULT_TIMEOUT
            ) as client:

                response = await client.post(
                    f"{self.base_url}/api/embeddings",
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

                return EmbeddingResponse(
                    embedding=data.get(
                        "embedding",
                        []
                    ),
                    model=model,
                )

        except httpx.ConnectError as e:

            raise LLMConnectionError(
                f"Ollama embedding connection failed: "
                f"{str(e)}"
            )

        except httpx.HTTPStatusError as e:

            raise LLMProviderError(
                f"Ollama embedding HTTP error: "
                f"{e.response.status_code}"
            )

        except Exception as e:

            raise LLMProviderError(
                f"Ollama embeddings failed: {str(e)}"
            )