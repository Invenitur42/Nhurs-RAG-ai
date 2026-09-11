#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "→ Starting Postgres (pgvector) + Redis..."
docker compose up -d

echo "→ Backend setup..."
cd backend
if [ ! -f .env ]; then cp .env.example .env; echo "Edit backend/.env with OPENAI_API_KEY"; fi
if [ ! -d .venv ]; then python3 -m venv .venv; fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt
python -m app.db.init_db || true
echo "Start backend with: cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000"

echo "→ Frontend setup..."
cd "$ROOT/frontend"
npm install
echo "Start frontend with: cd frontend && npm run dev"
echo "Done. UI http://localhost:3000 · API http://localhost:8000/docs"
