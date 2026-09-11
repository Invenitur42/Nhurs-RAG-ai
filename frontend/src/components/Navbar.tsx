"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearToken } from "@/lib/api";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();

  function handleLogout() {
    clearToken();
    router.push("/login");
  }

  const linkClass = (path: string) =>
    `px-3 py-2 rounded-lg text-sm font-medium transition ${
      pathname === path
        ? "bg-brand-50 text-brand-700"
        : "text-slate-600 hover:bg-slate-100"
    }`;

  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-6">
          <Link href="/dashboard" className="text-lg font-bold text-slate-900">
            RAG Knowledge Base
          </Link>
          <nav className="flex gap-1">
            <Link href="/dashboard" className={linkClass("/dashboard")}>
              Documents
            </Link>
            <Link href="/chat" className={linkClass("/chat")}>
              Chat
            </Link>
          </nav>
        </div>
        <button
          onClick={handleLogout}
          className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 transition"
        >
          Log out
        </button>
      </div>
    </header>
  );
}
