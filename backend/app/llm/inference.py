from app.llm.providers.ollama_provider import OllamaProvider


class LLMInferenceService:

    def __init__(self):
        self.provider = OllamaProvider()

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