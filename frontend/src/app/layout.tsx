import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RAG Knowledge Base",
  description: "Chat with your documents using Retrieval-Augmented Generation",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
