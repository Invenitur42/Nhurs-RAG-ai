# RAG Knowledge Base

A full-stack **Retrieval-Augmented Generation** application that lets users upload documents and chat with their own knowledge base.

**Target audience:** Full-stack developer interviews (junior → mid level with 2 years experience).

This project demonstrates real production patterns used in modern AI applications:
- Document ingestion pipeline (chunking, embedding, storage)
- Hybrid search (vector + keyword)
- Source citations in answers
- User authentication & multi-tenancy (each user has isolated documents)
- Clean separation of frontend / backend / AI layer

---

## Features (planned / in progress)

- [x] Project structure & documentation
- [ ] User auth (JWT / NextAuth)
- [ ] Document upload (PDF, TXT, Markdown, DOCX)
- [ ] Chunking + embedding pipeline
- [ ] Vector store with pgvector
- [ ] Chat interface with streaming responses
- [ ] Source citations & highlight
- [ ] Document management dashboard
- [ ] Basic evaluation / feedback on answers
- [ ] Docker Compose for local development

---

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | Next.js 15 (App Router) + TypeScript + Tailwind + shadcn/ui |
| Backend     | FastAPI + Python 3.11+              |
| AI / RAG    | LangChain / LlamaIndex + OpenAI embeddings + chat models |
| Database    | PostgreSQL + pgvector               |
| Auth        | JWT (backend) + NextAuth or custom  |
| Queue (opt) | Redis / Celery or background tasks  |
| Infra       | Docker + docker-compose             |

---

## Architecture Overview

```
User → Next.js Frontend
         ↓
      FastAPI Backend
         ├── Auth service
         ├── Document service (upload, parse, chunk)
         ├── Embedding service
         ├── Retrieval service (hybrid search)
         └── Chat / Generation service
         ↓
PostgreSQL (users, documents metadata) + pgvector (embeddings)
```

---

## Project Structure (target)

```
rag-knowledge-base/
├── backend/
│   ├── app/
│   │   ├── api/           # routers
│   │   ├── core/          # config, security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── services/      # business logic + RAG
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── types/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Getting Started (once scaffolded)

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker (recommended)
- OpenAI API key (or compatible provider)

### Local development

```bash
# Clone
git clone https://github.com/Invenitur42/rag-knowledge-base.git
cd rag-knowledge-base

# Start services
docker-compose up -d   # postgres + redis

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd ../frontend
npm install
npm run dev
```

---

## Interview Talking Points

When discussing this project you can talk about:
- Why hybrid search (vector + BM25) is better than pure vector search for many use cases
- Chunking strategies and their impact on retrieval quality
- How you handle multi-tenancy / document isolation
- Streaming responses and UX considerations
- Evaluation of RAG quality (faithfulness, relevance)
- Trade-offs between LangChain vs custom pipeline

---

## Status

Scaffolding in progress. Core structure and first endpoints coming next.

---

Part of the [AI Tools Portfolio](https://github.com/Invenitur42/ai-tools-portfolio)