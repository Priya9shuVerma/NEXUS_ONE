"use client";

import Link from "next/link";
import {
  ArrowLeft,
  FileText,
  Upload,
  Search,
  MoreVertical,
  Database,
  CheckCircle2,
  Clock3,
} from "lucide-react";

const documents = [
  {
    name: "Knowledge Base",
    type: "PDF",
    status: "Ready",
    size: "—",
  },
  {
    name: "Resume / Profile",
    type: "PDF",
    status: "Ready",
    size: "—",
  },
];

export default function DocumentsPage() {
  return (
    <main className="min-h-screen bg-[#05070b] text-white">
      <div className="mx-auto max-w-7xl p-5 lg:p-8">

        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2 text-xs text-gray-500">
              <Link href="/dashboard" className="hover:text-white">
                Dashboard
              </Link>
              <span>/</span>
              <span>Documents</span>
            </div>

            <h1 className="text-3xl font-bold">Documents</h1>
            <p className="mt-2 text-sm text-gray-500">
              Manage documents connected to your NEXUS ONE knowledge base.
            </p>
          </div>

          <Link
            href="/ai"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black hover:bg-gray-200"
          >
            <Upload size={17} />
            Upload Document
          </Link>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Total Documents</span>
              <FileText size={18} />
            </div>
            <div className="mt-4 text-3xl font-bold">0</div>
            <p className="mt-1 text-xs text-gray-500">
              Knowledge sources
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Indexed</span>
              <Database size={18} />
            </div>
            <div className="mt-4 text-3xl font-bold">0</div>
            <p className="mt-1 text-xs text-gray-500">
              Available for AI retrieval
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Processing</span>
              <Clock3 size={18} />
            </div>
            <div className="mt-4 text-3xl font-bold">0</div>
            <p className="mt-1 text-xs text-gray-500">
              Documents being processed
            </p>
          </div>
        </div>

        <section className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03]">

          <div className="flex flex-col gap-4 border-b border-white/10 p-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="font-semibold">Knowledge Sources</h2>
              <p className="mt-1 text-xs text-gray-500">
                Documents available to the AI knowledge engine.
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-black/20 px-3 py-2">
              <Search size={16} className="text-gray-500" />
              <input
                placeholder="Search documents..."
                className="w-full bg-transparent text-sm outline-none placeholder:text-gray-600 sm:w-56"
              />
            </div>
          </div>

          <div className="divide-y divide-white/10">
            {documents.map((document) => (
              <div
                key={document.name}
                className="flex flex-col gap-4 p-5 transition hover:bg-white/[0.02] sm:flex-row sm:items-center sm:justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/5">
                    <FileText size={21} />
                  </div>

                  <div>
                    <div className="font-medium">{document.name}</div>
                    <div className="mt-1 text-xs text-gray-500">
                      {document.type} · {document.size}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="inline-flex items-center gap-2 text-xs text-emerald-400">
                    <CheckCircle2 size={15} />
                    {document.status}
                  </div>

                  <button className="rounded-lg p-2 text-gray-500 hover:bg-white/5 hover:text-white">
                    <MoreVertical size={18} />
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="border-t border-white/10 p-8 text-center">
            <FileText
              size={34}
              className="mx-auto text-gray-700"
            />

            <h3 className="mt-4 font-medium">
              Your document workspace
            </h3>

            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-gray-500">
              Upload PDFs through the AI Knowledge Assistant and they will
              become available to the NEXUS ONE retrieval engine.
            </p>

            <Link
              href="/ai"
              className="mt-5 inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm hover:bg-white/10"
            >
              <BrainIcon />
              Open AI Assistant
            </Link>
          </div>

        </section>

        <footer className="mt-10 border-t border-white/10 pt-6 text-center text-xs text-gray-600">
          NEXUS ONE — AI Powered Enterprise Intelligence Platform
        </footer>

      </div>
    </main>
  );
}

function BrainIcon() {
  return <span>✦</span>;
}
