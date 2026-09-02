from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
import os

from app.llm.schemas import ChatMessage, GenerateRequest
from app.llm.service import LLMService
from app.rag.retrieval.vector_store import search_similar_chunks
from app.rag.ingestion.pdf_ingestor import extract_pdf_text
from app.rag.ingestion.chunker import chunk_text
from app.rag.embeddings.embedder import generate_embedding
from app.rag.retrieval.vector_store import (
    create_collection,
    store_chunks,
)

router = APIRouter(tags=["rag"])


class QueryRequest(BaseModel):
    query: str
    conversation_id: str | None = None
    provider: str = "ollama"
    model: str | None = None


@router.post("/upload")
async def upload_pdf(file: UploadFile):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_pdf_text(file_path)

    chunks = chunk_text(text)

    embeddings = [await generate_embedding(chunk) for chunk in chunks]

    create_collection()

    store_chunks(chunks, embeddings)

    return {
        "status": "success",
        "chunks": len(chunks),
    }


@router.post("/query")
async def query_rag(request: QueryRequest):

    query_embedding = await generate_embedding(request.query)

    results = search_similar_chunks(query_embedding)

    context = "\n".join(results)

    llm_service = LLMService()

    llm_request = GenerateRequest(
        messages=[
            ChatMessage(
                role="system",
                content=(
                    "You are a helpful RAG assistant. "
                    "Answer the user's question using ONLY the provided context. "
                    "If the answer is not present in the context, say: "
                    "'I could not find the answer in the provided documents.'"
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    f"Context:\n{context}\n\n"
                    f"Question:\n{request.query}"
                ),
            ),
        ],
        model=request.model or "qwen2.5-coder:7b",
        stream=False,
    )

    llm_response = await llm_service.generate_response(llm_request)

    return {
        "query": request.query,
        "context": results,
        "answer": llm_response.content,
    }