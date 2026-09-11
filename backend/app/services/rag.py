"""
RAG service layer – placeholder for the real retrieval + generation pipeline.

Next steps to implement:
1. Text extraction (PDF, DOCX, MD, TXT)
2. Chunking with overlap
3. Embedding via OpenAI text-embedding-3-small
4. Store vectors in pgvector
5. Similarity search + optional hybrid (BM25)
6. Prompt construction + LLM call with streaming support
"""

from typing import List
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.document import DocumentChunk

settings = get_settings()


def retrieve_relevant_chunks(
    db: Session,
    user_id: int,
    query: str,
    document_ids: List[int] | None = None,
    top_k: int | None = None,
) -> List[DocumentChunk]:
    """
    Placeholder retrieval.
    Real implementation will embed `query` and run vector similarity search.
    """
    top_k = top_k or settings.TOP_K

    q = (
        db.query(DocumentChunk)
        .join(DocumentChunk.document)
        .filter(DocumentChunk.document.has(owner_id=user_id))
    )

    if document_ids:
        q = q.filter(DocumentChunk.document_id.in_(document_ids))

    return q.limit(top_k).all()


def generate_answer(question: str, context_chunks: List[DocumentChunk]) -> str:
    """
    Placeholder generation.
    Real version builds a prompt and calls the chat model.
    """
    if not context_chunks:
        return "No relevant documents found. Please upload some files first."

    return (
        f"Based on {len(context_chunks)} retrieved passages related to '{question}', "
        "a real LLM answer will be generated here."
    )
