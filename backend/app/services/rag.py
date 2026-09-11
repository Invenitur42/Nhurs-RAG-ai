"""
Real RAG pipeline:
- Embed the user question
- Perform cosine similarity search over the user's document chunks (pgvector)
- Build a grounded prompt
- Call the chat model and return answer + source chunks
"""

from __future__ import annotations

from typing import List, Tuple

from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.config import get_settings
from app.models.document import Document, DocumentChunk

settings = get_settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


def _embed_query(query: str) -> List[float]:
    if not client:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=query,
    )
    return response.data[0].embedding


def retrieve_relevant_chunks(
    db: Session,
    user_id: int,
    query: str,
    document_ids: List[int] | None = None,
    top_k: int | None = None,
) -> List[DocumentChunk]:
    """
    Vector similarity search using pgvector cosine distance.
    Only returns chunks belonging to the current user (and optionally filtered documents).
    """
    top_k = top_k or settings.TOP_K
    query_embedding = _embed_query(query)

    stmt = (
        select(DocumentChunk)
        .join(Document)
        .options(joinedload(DocumentChunk.document))
        .where(Document.owner_id == user_id)
        .where(Document.status == "ready")
        .where(DocumentChunk.embedding.is_not(None))
    )

    if document_ids:
        stmt = stmt.where(Document.id.in_(document_ids))

    # Order by cosine distance (most similar first) and limit
    stmt = stmt.order_by(DocumentChunk.embedding.cosine_distance(query_embedding)).limit(top_k)

    results = db.execute(stmt).scalars().unique().all()
    return list(results)


def build_context(chunks: List[DocumentChunk]) -> str:
    """Format retrieved chunks into a single context string for the prompt."""
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.document.filename if chunk.document else "unknown"
        parts.append(f"[{i}] (Source: {source})\n{chunk.content}")
    return "\n\n---\n\n".join(parts)


def generate_answer(question: str, context_chunks: List[DocumentChunk]) -> str:
    """Call the chat model with a grounded prompt."""
    if not client:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    if not context_chunks:
        return (
            "I don't have any relevant information in your documents to answer that. "
            "Please upload relevant files and try again."
        )

    context = build_context(context_chunks)

    system_prompt = (
        "You are a helpful assistant that answers questions using only the provided context. "
        "If the answer cannot be found in the context, say so clearly. "
        "Be concise and accurate. When possible, refer to the source numbers like [1], [2]."
    )

    user_prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    response = client.chat.completions.create(
        model=settings.CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    return response.choices[0].message.content or "No answer generated."


def answer_question(
    db: Session,
    user_id: int,
    question: str,
    document_ids: List[int] | None = None,
) -> Tuple[str, List[DocumentChunk]]:
    """
    High-level RAG entrypoint.
    Returns (answer, list of source chunks).
    """
    chunks = retrieve_relevant_chunks(
        db=db,
        user_id=user_id,
        query=question,
        document_ids=document_ids,
    )
    answer = generate_answer(question, chunks)
    return answer, chunks
