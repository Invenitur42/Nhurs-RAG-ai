"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import {
  listDocuments,
  uploadDocument,
  deleteDocument,
  getMe,
  type Document,
} from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [docs, setDocs] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [userName, setUserName] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    async function init() {
      try {
        const user = await getMe();
        setUserName(user.full_name || user.email);
        const data = await listDocuments();
        setDocs(data);
      } catch {
        router.replace("/login");
      } finally {
        setLoading(false);
      }
    }
    init();
  }, [router]);

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError("");
    try {
      const doc = await uploadDocument(file);
      setDocs((prev) => [doc, ...prev]);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("Delete this document?")) return;
    try {
      await deleteDocument(id);
      setDocs((prev) => prev.filter((d) => d.id !== id));
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }

  function statusBadge(status: string) {
    const colors: Record<string, string> = {
      ready: "bg-emerald-50 text-emerald-700",
      processing: "bg-amber-50 text-amber-700",
      failed: "bg-red-50 text-red-700",
    };
    return (
      <span
        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
          colors[status] || "bg-slate-100 text-slate-600"
        }`}
      >
        {status}
      </span>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-slate-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <main className="mx-auto max-w-6xl px-4 py-8">
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Your Documents</h1>
            <p className="mt-1 text-sm text-slate-500">
              Welcome back{userName ? `, ${userName}` : ""}. Upload files to build your knowledge base.
            </p>
          </div>

          <div>
            <input
              ref={fileRef}
              type="file"
              accept=".pdf,.txt,.md,.docx"
              onChange={handleUpload}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className={`inline-flex cursor-pointer items-center rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 transition ${
                uploading ? "opacity-60 pointer-events-none" : ""
              }`}
            >
              {uploading ? "Processing..." : "Upload document"}
            </label>
          </div>
        </div>

        {error && (
          <div className="mb-6 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
        )}

        {docs.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white py-16 text-center">
            <p className="text-slate-500">No documents yet.</p>
            <p className="mt-1 text-sm text-slate-400">
              Upload a PDF, TXT, MD, or DOCX to get started.
            </p>
          </div>
        ) : (
          <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-100 bg-slate-50 text-xs uppercase text-slate-500">
                <tr>
                  <th className="px-5 py-3 font-medium">Filename</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Uploaded</th>
                  <th className="px-5 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {docs.map((doc) => (
                  <tr key={doc.id} className="hover:bg-slate-50/50">
                    <td className="px-5 py-3.5 font-medium text-slate-900">{doc.filename}</td>
                    <td className="px-5 py-3.5">{statusBadge(doc.status)}</td>
                    <td className="px-5 py-3.5 text-slate-500">
                      {new Date(doc.created_at).toLocaleString()}
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="text-sm font-medium text-red-600 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="mt-6 text-center">
          <a
            href="/chat"
            className="text-sm font-medium text-brand-600 hover:underline"
          >
            Go to Chat →
          </a>
        </div>
      </main>
    </div>
  );
}
