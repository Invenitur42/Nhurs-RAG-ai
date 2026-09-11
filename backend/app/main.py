from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG Knowledge Base API",
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
