const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export type User = {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
  created_at: string;
};

export type Document = {
  id: number;
  filename: string;
  content_type: string | null;
  status: string;
  created_at: string;
};

export type SourceChunk = {
  document_id: number;
  filename: string;
  content: string;
  chunk_index: number;
};

export type ChatResponse = {
  answer: string;
  sources: SourceChunk[];
};

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export function setToken(token: string) {
  localStorage.setItem("token", token);
}

export function clearToken() {
  localStorage.removeItem("token");
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: HeadersInit = {
    ...(options.headers || {}),
  };

  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  // Don't set Content-Type for FormData
  if (!(options.body instanceof FormData)) {
    (headers as Record<string, string>)["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    clearToken();
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

// Auth
export async function register(email: string, password: string, fullName?: string) {
  return request<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password, full_name: fullName || null }),
  });
}

export async function login(email: string, password: string) {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(err.detail || "Login failed");
  }

  const data = await res.json();
  setToken(data.access_token);
  return data;
}

export async function getMe() {
  return request<User>("/auth/me");
}

// Documents
export async function listDocuments() {
  return request<Document[]>("/documents/");
}

export async function uploadDocument(file: File) {
  const form = new FormData();
  form.append("file", file);
  return request<Document>("/documents/upload", {
    method: "POST",
    body: form,
  });
}

export async function deleteDocument(id: number) {
  return request<void>(`/documents/${id}`, { method: "DELETE" });
}

// Chat
export async function askQuestion(question: string, documentIds?: number[]) {
  return request<ChatResponse>("/chat/", {
    method: "POST",
    body: JSON.stringify({
      question,
      document_ids: documentIds || null,
    }),
  });
}
