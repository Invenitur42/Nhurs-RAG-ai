"""
Document ingestion pipeline:
1. Extract text from PDF / TXT / MD / DOCX
2. Split into overlapping chunks
3. Generate embeddings
4. Persist chunks + vectors in Postgres (pgvector)
"""

from __future__ import annotations

import io
from typing import List

from openai import OpenAI
from pypdf import PdfReader
from docx import Document as DocxDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.document import Document, DocumentChunk

settings = get_settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


def extract_text(filename: str, content: bytes, content_type: str | None) -> str:
    """Extract plain text from supported file types."""
    name = (filename or "").lower()

    # Plain text / markdown
    if name.endswith((".txt", ".md")) or (content_type and content_type.startswith("text/")):
        return content.decode("utf-8", errors="ignore")

    # PDF
    if name.endswith(".pdf") or content_type == "application/pdf":
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages).strip()

    # DOCX
    if name.endswith(".docx") or (
        content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        doc = DocxDocument(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs if p.text).strip()

    raise ValueError(f"Unsupported file type: {filename} ({content_type})")


def chunk_text(text: str) -> List[str]:
    """Split text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Create embeddings using OpenAI."""
    if not client:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    # OpenAI allows batching; keep batches reasonable
    embeddings: List[List[float]] = []
    batch_size = 64

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=batch,
        )
        # Ensure order is preserved
        batch_embeddings = [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
        embeddings.extend(batch_embeddings)

    return embeddings


def process_and_store_document(
    db: Session,
    document: Document,
    raw_content: bytes,
) -> None:
    """
    Full pipeline: extract → chunk → embed → save chunks.
    Marks the document as 'ready' or 'failed'.
    """
    try:
        text = extract_text(document.filename, raw_content, document.content_type)
        if not text or len(text.strip()) < 20:
            raise ValueError("Extracted text is empty or too short")

        chunks = chunk_text(text)
        if not chunks:
            raise ValueError("No chunks produced from document")

        vectors = embed_texts(chunks)

        # Clear any previous chunks (in case of re-processing)
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document.id).delete()

        for idx, (chunk_content, vector) in enumerate(zip(chunks, vectors)):
            db_chunk = DocumentChunk(
                document_id=document.id,
                content=chunk_content,
                chunk_index=idx,
                embedding=vector,
            )
            db.add(db_chunk)

        document.status = "ready"
        db.commit()

    except Exception as exc:
        document.status = "failed"
        db.commit()
        # Re-raise so the caller can log / surface the error if desired
        raise RuntimeError(f"Failed to process document {document.id}: {exc}") from exc
