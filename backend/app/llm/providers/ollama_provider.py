import requests

from app.core.settings import settings


class OllamaProvider:

    def generate(
        self,
        messages,
        model=None,
        stream=False
    ):

        model = model or settings.DEFAULT_MODEL

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": stream
            },
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]