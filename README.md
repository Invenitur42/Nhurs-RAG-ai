# RAG Knowledge Base

A full-stack **Retrieval-Augmented Generation** application that lets users upload documents and chat with their own knowledge base.

**Target audience:** Full-stack developer interviews (junior → mid level with ~2 years experience).

This project demonstrates real production patterns used in modern AI applications:
- Document ingestion pipeline (parsing → chunking → embedding → storage)
- Vector similarity search with pgvector
- Grounded LLM answers with source citations
- User authentication & multi-tenancy (documents isolated per user)
- Clean separation of frontend / backend / AI layer

---

## Features

- [x] Project structure & documentation
- [x] User auth (register / login / JWT)
- [x] Document models + upload endpoint
- [x] **Full document processing pipeline** (PDF, TXT, MD, DOCX)
- [x] **Chunking with overlap**
- [x] **OpenAI embeddings stored in pgvector**
- [x] **Real cosine similarity search**
- [x] **Grounded LLM answer generation**
- [x] Source chunks returned for citations
- [x] Docker Compose (Postgres + pgvector + Redis)
- [x] **Frontend UI** (login, register, dashboard, chat with citations)
- [ ] Streaming responses
- [ ] Background task queue for large documents (optional)

---

## Tech Stack

| Layer       | Technology                                      |
|-------------|-------------------------------------------------|
| Frontend    | Next.js 15 (App Router) + TypeScript + Tailwind |
| Backend     | FastAPI + Python 3.11+                          |
| AI / RAG    | OpenAI embeddings (`text-embedding-3-small`) + chat models |
| Database    | PostgreSQL + pgvector                           |
| Auth        | JWT (python-jose + passlib)                     |
| Infra       | Docker + docker-compose                         |

---

## Architecture Overview

```
User → Next.js Frontend
         ↓
      FastAPI Backend
         ├── Auth (JWT)
         ├── Documents (upload → parse → chunk → embed → store)
         ├── RAG service (embed query → vector search → LLM)
         └── Chat endpoint (returns answer + sources)
         ↓
PostgreSQL (users, documents metadata) + pgvector (1536-dim embeddings)
```

---

## Backend API

| Method | Endpoint                    | Description                          |
|--------|-----------------------------|--------------------------------------|
| POST   | `/api/v1/auth/register`     | Create account                       |
| POST   | `/api/v1/auth/login`        | Get JWT                              |
| GET    | `/api/v1/auth/me`           | Current user                         |
| GET    | `/api/v1/documents/`        | List my documents                    |
| POST   | `/api/v1/documents/upload`  | Upload + fully process a document    |
| DELETE | `/api/v1/documents/{id}`    | Delete a document                    |
| POST   | `/api/v1/chat/`             | Ask a question (real RAG)            |

Interactive docs: `http://localhost:8000/docs`

---

## Frontend Pages

| Route        | Description                            |
|--------------|----------------------------------------|
| `/login`     | Sign in                                |
| `/register`  | Create account                         |
| `/dashboard` | List / upload / delete documents       |
| `/chat`      | Chat UI with source citations          |

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
cp .env.example .env
# Edit .env → set OPENAI_API_KEY and a strong SECRET_KEY

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create tables + enable pgvector extension
python -m app.db.init_db

# Run the API
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## How the RAG Pipeline Works

1. **Upload** → file is saved as a `Document` with status `processing`
2. **Extract** → text is pulled from PDF / DOCX / TXT / MD
3. **Chunk** → `RecursiveCharacterTextSplitter` (configurable size + overlap)
4. **Embed** → OpenAI `text-embedding-3-small` (batched)
5. **Store** → chunks + 1536-dim vectors written to `document_chunks` via pgvector
6. **Query** → question is embedded → cosine similarity search (scoped to the user)
7. **Generate** → top-k chunks are injected into a grounded prompt → LLM answers
8. **Return** → answer + source chunks (shown as citations in the UI)

---

## Interview Talking Points

- Why pure vector search can fail on exact keyword matches and how hybrid search helps
- Impact of chunk size and overlap on retrieval quality and context window usage
- Multi-tenancy: every query is filtered by `owner_id` so users never see each other’s data
- Trade-offs of synchronous processing vs background workers for large files
- How you would add evaluation (faithfulness / relevance scores) later
- Why FastAPI + Next.js is a strong full-stack choice for AI products

---

## Optional Next Improvements

- Streaming responses for better UX
- Background worker (Celery / ARQ) for large document processing
- Hybrid search (vector + BM25)
- Answer evaluation metrics

---

Part of the [AI Tools Portfolio](https://github.com/Invenitur42/ai-tools-portfolio)