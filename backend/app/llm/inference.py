from app.llm.providers.ollama_provider import OllamaProvider
import requests
import json
import os

class LLMInferenceService:

    def __init__(self):
        self.provider = OllamaProvider()
        self.base_url = os.getenv(
            "OLLAMA_URL",
            "http://ollama:11434"
        )

    def generate_response(
        self,
        messages,
        model=None,
        stream=False
    ):

        return self.provider.generate(
            messages=messages,
            model=model,
            stream=stream
        )

    def stream_response(
            self,
            messages,
            model="qwen2.5-coder:7b"
    ):

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": True
            },
            stream=True
        )
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                try:
                    data = json.loads(decoded_line)
                    if "message" in data:

                        content = data["message"].get("content", "")
                        if content:
                            yield content
                except Exception:
                    continue