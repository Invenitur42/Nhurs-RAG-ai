# Frontend

Next.js app for document upload and chat.

```bash
cd frontend
cp .env.local.example .env.local   # defaults to http://localhost:8000
npm install
npm run dev
```

Routes: `/login`, `/register`, `/dashboard` (docs), `/chat`.

Token is stored in localStorage after login. Backend should be on port 8000.
