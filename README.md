# RAG Knowledge Base

A full-stack **Retrieval-Augmented Generation** application that lets users upload documents and chat with their own knowledge base.

**Target audience:** Full-stack developer interviews (junior → mid level with ~2 years experience).

This project demonstrates real production patterns used in modern AI applications:
- Document ingestion pipeline (chunking, embedding, storage)
- Vector search with pgvector
- Source citations in answers
- User authentication & multi-tenancy (each user has isolated documents)
- Clean separation of frontend / backend / AI layer

---

## Features

- [x] Project structure & documentation
- [x] User auth (register / login / JWT)
- [x] Document models + upload endpoint (stub)
- [x] Chat endpoint with retrieval placeholder
- [x] Docker Compose (Postgres + pgvector + Redis)
- [x] Frontend package scaffolding (Next.js 15 + TypeScript)
- [ ] Full document parsing + chunking + embedding pipeline
- [ ] Real vector similarity search
- [ ] LLM answer generation + streaming
- [ ] Frontend pages (auth, dashboard, chat UI)
- [ ] Source citations in the UI

---

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | Next.js 15 (App Router) + TypeScript + Tailwind |
| Backend     | FastAPI + Python 3.11+              |
| AI / RAG    | OpenAI embeddings + chat models (LangChain ready) |
| Database    | PostgreSQL + pgvector               |
| Auth        | JWT (python-jose + passlib)         |
| Infra       | Docker + docker-compose             |

---

## Architecture Overview

```
User → Next.js Frontend
         ↓
      FastAPI Backend
         ├── Auth (JWT)
         ├── Documents (upload / list / delete)
         ├── RAG service (retrieve + generate)
         └── Chat endpoint
         ↓
PostgreSQL (users, documents) + pgvector (embeddings)
```

---

## Current Backend API

| Method | Endpoint                    | Description                |
|--------|-----------------------------|----------------------------|
| POST   | `/api/v1/auth/register`     | Create account             |
| POST   | `/api/v1/auth/login`        | Get JWT                    |
| GET    | `/api/v1/auth/me`           | Current user               |
| GET    | `/api/v1/documents/`        | List my documents          |
| POST   | `/api/v1/documents/upload`  | Upload a document          |
| DELETE | `/api/v1/documents/{id}`    | Delete a document          |
| POST   | `/api/v1/chat/`             | Ask a question (RAG)       |

Interactive docs available at `http://localhost:8000/docs` once the backend is running.

---

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker
- OpenAI API key

### 1. Start infrastructure

```bash
git clone https://github.com/Invenitur42/rag-knowledge-base.git
cd rag-knowledge-base
docker-compose up -d
```

### 2. Backend

```bash
cd backend
cp .env.example .env          # add your OPENAI_API_KEY and SECRET_KEY
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend (basic scaffold)

```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
rag-knowledge-base/
├── backend/
│   ├── app/
│   │   ├── api/          # auth, documents, chat routers
│   │   ├── core/         # config, security
│   │   ├── db/           # SQLAlchemy session
│   │   ├── models/       # User, Document, DocumentChunk
│   │   ├── schemas/      # Pydantic models
│   │   ├── services/     # RAG logic
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── package.json
│   └── README.md
├── docker-compose.yml
└── README.md
```

---

## Interview Talking Points

- Why hybrid search (vector + keyword) often beats pure vector search
- Chunk size / overlap trade-offs and their effect on retrieval quality
- Multi-tenancy: how documents are isolated per user
- Streaming responses and perceived latency
- How you would evaluate RAG quality (faithfulness, context relevance)
- Why you chose FastAPI + Next.js for this stack

---

## Next Development Steps

1. Implement real document parsing + chunking + embedding
2. Wire vector search in the RAG service
3. Call the LLM and return proper answers + sources
4. Build the Next.js UI (auth pages, document dashboard, chat with citations)
5. Add background task for heavy processing (optional)

---

Part of the [AI Tools Portfolio](https://github.com/Invenitur42/ai-tools-portfolio)