from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.document import Document, DocumentChunk
from app.schemas.document import ChatRequest, ChatResponse, SourceChunk
from app.core.config import get_settings

router = APIRouter(prefix="/chat", tags=["chat"])
settings = get_settings()


@router.post("/", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Simple RAG endpoint.

    Current implementation is a placeholder that returns a structured response.
    Next iteration will:
    1. Embed the question
    2. Perform similarity search over the user's chunks
    3. Build a prompt with retrieved context
    4. Call the LLM and return answer + sources
    """
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Scope to current user's documents
    query = (
        db.query(DocumentChunk)
        .join(Document)
        .filter(Document.owner_id == current_user.id, Document.status == "ready")
    )

    if body.document_ids:
        query = query.filter(Document.id.in_(body.document_ids))

    # Placeholder: take first few chunks (real version uses vector search)
    chunks = query.limit(settings.TOP_K).all()

    sources = [
        SourceChunk(
            document_id=c.document_id,
            filename=c.document.filename,
            content=c.content[:500],
            chunk_index=c.chunk_index,
        )
        for c in chunks
    ]

    # Placeholder answer – replace with real LLM call later
    if not sources:
        answer = (
            "I don't have any documents to answer from yet. "
            "Please upload some files first."
        )
    else:
        answer = (
            f"(Placeholder RAG response) Based on {len(sources)} retrieved chunks "
            f"from your documents, here is a summary related to: '{body.question}'.\n\n"
            "Real LLM generation will be wired in the next step."
        )

    return ChatResponse(answer=answer, sources=sources)
