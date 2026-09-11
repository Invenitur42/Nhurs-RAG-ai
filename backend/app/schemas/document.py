from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str
    document_ids: list[int] | None = None  # optional filter


class SourceChunk(BaseModel):
    document_id: int
    filename: str
    content: str
    chunk_index: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
