"""Retrieval agent.

Responsible for retrieving relevant context for a query.
This should orchestrate RAG retrieval components (vector store, embeddings) but not LLM generation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetrievalAgent:
    """Agent that retrieves context for a query."""

    async def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        # TODO: integrate app.rag.retrieval.vector_store + embeddings
        return []

