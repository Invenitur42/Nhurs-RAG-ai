# Frontend – RAG Knowledge Base

Next.js 15 (App Router) + TypeScript + Tailwind UI for the RAG Knowledge Base.

## Pages

| Route        | Description                                      |
|--------------|--------------------------------------------------|
| `/`          | Redirects to dashboard or login                  |
| `/login`     | Sign in                                          |
| `/register`  | Create account                                   |
| `/dashboard` | List, upload, and delete documents               |
| `/chat`      | Chat interface with source citations             |

## Getting Started

```bash
cd frontend
cp .env.local.example .env.local   # optional, defaults to localhost:8000
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

Make sure the backend is running on port 8000.

## Features

- JWT auth (token stored in localStorage)
- Document upload with status badges
- Chat with message history
- Source citations under each assistant reply
- Clean, responsive UI
