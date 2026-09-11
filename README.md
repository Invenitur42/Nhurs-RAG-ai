# Nhurs RAG AI

Upload documents and ask questions against them. Answers come from retrieved chunks (RAG), not from the model guessing.

Stack: **FastAPI**, **Postgres + pgvector**, **OpenAI embeddings**, **Next.js**.

**Live demo (browser preview):** [Open Doc Chat](https://invenitur42.github.io/Nhurs-RAG-ai/)  
Sample docs + retrieval UI in the browser. Full pipeline (embeddings / pgvector / OpenAI) is in this repo.

[Open in Codespaces](https://codespaces.new/Invenitur42/Nhurs-RAG-ai)

---

## What it does

- Sign up / log in (JWT)
- Upload PDF, TXT, MD, or DOCX
- Files get chunked, embedded, and stored in pgvector
- Chat UI returns an answer plus the source snippets used

Each user’s docs stay isolated (`owner_id` on queries).

---

## Setup

Needs Docker, Python 3.11+, Node 20+, and an OpenAI key.

```bash
git clone https://github.com/Invenitur42/Nhurs-RAG-ai.git
cd Nhurs-RAG-ai
docker compose up -d

cd backend
cp .env.example .env   # OPENAI_API_KEY, SECRET_KEY
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000

# other terminal
cd frontend
npm install && npm run dev
```

- App: http://localhost:3000  
- API docs: http://localhost:8000/docs  

Optional bootstrap: `bash scripts/dev.sh`

---

## How the pipeline works

1. Upload → save file metadata  
2. Extract text → split with overlap  
3. Embed chunks → write vectors to Postgres  
4. On ask: embed the question → similarity search → prompt the model with those chunks  
5. Response includes the sources so you can check them in the UI  

---

## Notes / possible next steps

- Chunk size and overlap matter a lot for quality  
- Large uploads would be better off a background worker  
- Hybrid search (keyword + vector) helps when people use exact terms  
- Streaming the answer would improve the chat feel  

---

## Deploy

Frontend on Vercel (`frontend/`), API on Railway/Render, Postgres with the `pgvector` extension. Set `NEXT_PUBLIC_API_URL`, `DATABASE_URL`, `OPENAI_API_KEY`, `SECRET_KEY`.
