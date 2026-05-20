from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
import os

from app.rag.ingestion.pdf_ingestor import extract_pdf_text
from app.rag.ingestion.chunker import chunk_text
from app.rag.embeddings.embedder import generate_embedding
from app.rag.retrieval.vector_store import (
    create_collection,
    store_chunks
)

router = APIRouter(tags=["rag"])


class QueryRequest(BaseModel):
    query: str


@router.post("/upload")
async def upload_pdf(file: UploadFile):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_pdf_text(file_path)

    chunks = chunk_text(text)

    embeddings = [
        generate_embedding(chunk)
        for chunk in chunks
    ]

    create_collection()

    store_chunks(chunks, embeddings)

    return {
        "status": "success",
        "chunks": len(chunks)
    }


@router.post("/query")
async def query_rag(request: QueryRequest):
    return {
        "query": request.query,
        "answer": "RAG response here"
    }