from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api import auth, documents, chat

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Full-stack RAG application for chatting with your documents",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(documents.router, prefix=settings.API_V1_PREFIX)
app.include_router(chat.router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "rag-knowledge-base"}


@app.get("/")
def root():
    return {
        "message": "RAG Knowledge Base API",
        "docs": "/docs",
        "version": "0.1.0",
    }
