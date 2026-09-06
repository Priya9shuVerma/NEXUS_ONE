"use client";

import Link from "next/link";
import {
  ArrowLeft,
  History,
  MessageSquare,
  Search,
  Trash2,
  Clock3,
  Brain,
} from "lucide-react";

const conversations = [
  {
    title: "Document Questions",
    preview: "Ask questions about your uploaded documents",
    time: "No conversations yet",
  },
  {
    title: "Knowledge Analysis",
    preview: "Explore information from your knowledge base",
    time: "No conversations yet",
  },
];

export default function HistoryPage() {
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
              <span>Chat History</span>
            </div>

            <h1 className="text-3xl font-bold">Chat History</h1>

            <p className="mt-2 text-sm text-gray-500">
              Review your previous conversations with NEXUS ONE AI.
            </p>
          </div>

          <Link
            href="/ai"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black hover:bg-gray-200"
          >
            <Brain size={17} />
            New Conversation
          </Link>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                Conversations
              </span>
              <MessageSquare size={18} />
            </div>

            <div className="mt-4 text-3xl font-bold">0</div>

            <p className="mt-1 text-xs text-gray-500">
              Total conversations
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                AI Queries
              </span>
              <Brain size={18} />
            </div>

            <div className="mt-4 text-3xl font-bold">0</div>

            <p className="mt-1 text-xs text-gray-500">
              Questions processed
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                Last Activity
              </span>
              <Clock3 size={18} />
            </div>

            <div className="mt-4 text-lg font-bold">
              No activity
            </div>

            <p className="mt-1 text-xs text-gray-500">
              Your latest AI activity
            </p>
          </div>

        </div>

        <section className="mt-8 overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03]">

          <div className="flex flex-col gap-4 border-b border-white/10 p-5 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <h2 className="font-semibold">
                Conversations
              </h2>

              <p className="mt-1 text-xs text-gray-500">
                Your AI conversation history.
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-black/20 px-3 py-2">
              <Search size={16} className="text-gray-500" />

              <input
                placeholder="Search conversations..."
                className="w-full bg-transparent text-sm outline-none placeholder:text-gray-600 sm:w-56"
              />
            </div>

          </div>

          <div className="divide-y divide-white/10">

            {conversations.map((conversation) => (
              <div
                key={conversation.title}
                className="flex flex-col gap-4 p-5 transition hover:bg-white/[0.02] sm:flex-row sm:items-center sm:justify-between"
              >

                <div className="flex items-center gap-4">

                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/5">
                    <MessageSquare size={20} />
                  </div>

                  <div>
                    <h3 className="font-medium">
                      {conversation.title}
                    </h3>

                    <p className="mt-1 text-xs text-gray-500">
                      {conversation.preview}
                    </p>
                  </div>

                </div>

                <div className="flex items-center gap-4">

                  <span className="text-xs text-gray-600">
                    {conversation.time}
                  </span>

                  <button
                    disabled
                    className="rounded-lg p-2 text-gray-700"
                    title="Delete conversation"
                  >
                    <Trash2 size={17} />
                  </button>

                </div>

              </div>
            ))}

          </div>

          <div className="border-t border-white/10 p-10 text-center">

            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <History size={28} className="text-gray-600" />
            </div>

            <h3 className="mt-5 text-lg font-semibold">
              No saved conversations
            </h3>

            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-gray-500">
              Start a conversation with NEXUS ONE AI. Your conversation
              history will appear here once the memory system is connected.
            </p>

            <Link
              href="/ai"
              className="mt-6 inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black hover:bg-gray-200"
            >
              <MessageSquare size={17} />
              Start Chat
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
