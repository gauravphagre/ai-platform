from app.llm.service import LLMService

async def generate_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    llm_service = LLMService()
    response = await llm_service.generate_embeddings(text=text, model=model)
    return response.embedding
