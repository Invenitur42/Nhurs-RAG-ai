from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.document import ChatRequest, ChatResponse, SourceChunk
from app.services.rag import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Full RAG endpoint:
    1. Embed the question
    2. Retrieve top-k most similar chunks (pgvector)
    3. Generate a grounded answer with the LLM
    4. Return answer + source chunks for citations
    """
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer, chunks = answer_question(
            db=db,
            user_id=current_user.id,
            question=body.question.strip(),
            document_ids=body.document_ids,
        )
    except RuntimeError as exc:
        # Most commonly missing OPENAI_API_KEY
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    sources = [
        SourceChunk(
            document_id=c.document_id,
            filename=c.document.filename if c.document else "unknown",
            content=c.content[:600],
            chunk_index=c.chunk_index,
        )
        for c in chunks
    ]

    return ChatResponse(answer=answer, sources=sources)
