# Nhurs RAG AI — Chat with your documents

Full-stack **Retrieval-Augmented Generation** app: upload PDFs/docs, embed them, and chat with grounded answers + source citations.

[![Open in Codespaces](https://img.shields.io/badge/Open%20in-GitHub%20Codespaces-blue?logo=github)](https://codespaces.new/Invenitur42/Nhurs-RAG-ai)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-black)](https://nextjs.org/)

> **Live demo:** _Add your Vercel + Railway/Render URLs here after deploy_

---

## About this project

Built to show **production-style full-stack + AI** skills for interviews:

- End-to-end flow from upload → chunk → embed → retrieve → generate
- JWT auth and **per-user document isolation**
- Real vector search with **pgvector**, not a mock
- Next.js UI: login, document dashboard, chat with citations

**Why it matters for hiring:** AI features that are wired into real auth, storage, and UX — not a single notebook cell.

---

## Features

- JWT register / login
- Upload PDF, TXT, MD, DOCX
- Chunking + OpenAI embeddings → Postgres/pgvector
- Cosine similarity retrieval + grounded LLM answers
- Source citations in the chat UI
- Docker Compose for Postgres + Redis

---

## Tech stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 15, TypeScript, Tailwind |
| Backend | FastAPI, SQLAlchemy, JWT |
| AI | OpenAI embeddings + chat |
| DB | PostgreSQL + pgvector |
| Infra | Docker Compose |

---

## Run locally (one path)

**Prerequisites:** Docker, Python 3.11+, Node 20+, OpenAI API key

```bash
git clone https://github.com/Invenitur42/Nhurs-RAG-ai.git
cd Nhurs-RAG-ai

# 1) Database
docker compose up -d

# 2) Backend
cd backend
cp .env.example .env   # set OPENAI_API_KEY and SECRET_KEY
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000

# 3) Frontend (new terminal)
cd frontend
npm install
npm run dev
```

| Service | URL |
|---------|-----|
| App UI | http://localhost:3000 |
| API docs | http://localhost:8000/docs |

**Or:** click **Code → Codespaces** on GitHub (devcontainer included).

---

## Architecture

```
Browser (Next.js) → FastAPI → Auth / Documents / RAG service
                              → PostgreSQL + pgvector
                              → OpenAI embeddings & chat
```

---

## Interview talking points

1. **Why RAG?** LLMs alone hallucinate; retrieval grounds answers in user docs.
2. **Chunk size / overlap** — trade-off between context quality and noise.
3. **Multi-tenancy** — every query filtered by `owner_id`.
4. **Sync processing** on upload is simple; queues (Celery/ARQ) scale better for large files.
5. **Citations** — returning chunks lets the UI (and users) verify answers.
6. **Next steps** — streaming, hybrid search (BM25 + vector), evaluation metrics.

---

## Deploy (recommended for interviews)

1. **Frontend:** Vercel → root `frontend/`, env `NEXT_PUBLIC_API_URL=https://your-api`
2. **Backend:** Railway / Render → `backend/`, set `DATABASE_URL`, `OPENAI_API_KEY`, `SECRET_KEY`
3. **Database:** managed Postgres with `pgvector` extension
4. Put the live URL at the top of this README

---

## Screenshots

_Add 2–3 screenshots here: login, document list, chat with sources._

---

Part of [ai-tools-portfolio](https://github.com/Invenitur42/ai-tools-portfolio)
