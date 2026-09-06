"use client";

import Link from "next/link";
import {
  ArrowLeft,
  BarChart3,
  Brain,
  FileText,
  History,
  MessageSquare,
  Activity,
  TrendingUp,
  Zap,
  ShieldCheck,
  Clock3,
  Database,
  Search,
} from "lucide-react";

const activity = [
  {
    title: "AI Knowledge Assistant",
    description: "Document question processed",
    time: "Recently",
    icon: Brain,
  },
  {
    title: "Document Workspace",
    description: "Knowledge source available",
    time: "Recently",
    icon: FileText,
  },
  {
    title: "Chat History",
    description: "Conversation activity",
    time: "Recently",
    icon: MessageSquare,
  },
];

const usage = [
  { label: "AI Queries", value: "0", percentage: 0 },
  { label: "Documents", value: "0", percentage: 0 },
  { label: "Conversations", value: "0", percentage: 0 },
  { label: "Knowledge Retrieval", value: "0", percentage: 0 },
];

export default function AnalyticsPage() {
  return (
    <main className="min-h-screen bg-[#05070b] px-5 py-8 text-white lg:px-10">
      <div className="mx-auto max-w-7xl">

        {/* HEADER */}
        <div className="mb-8 flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

          <div>
            <div className="mb-3 flex items-center gap-2 text-xs text-gray-500">
              <Link href="/dashboard" className="hover:text-white">
                Dashboard
              </Link>
              <span>/</span>
              <span>Analytics</span>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-violet-500/10 ring-1 ring-violet-500/20">
                <BarChart3 size={28} className="text-violet-400" />
              </div>

              <div>
                <h1 className="text-3xl font-bold tracking-tight">
                  Analytics
                </h1>

                <p className="mt-1 text-sm text-gray-500">
                  Monitor NEXUS ONE intelligence activity and usage.
                </p>
              </div>
            </div>
          </div>

          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-gray-300 transition hover:bg-white/10 hover:text-white"
          >
            <ArrowLeft size={17} />
            Dashboard
          </Link>

        </div>

        {/* HERO */}
        <section className="relative overflow-hidden rounded-3xl border border-violet-500/20 bg-gradient-to-br from-violet-500/[0.09] via-white/[0.03] to-cyan-500/[0.05] p-6 lg:p-8">

          <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-violet-500/10 blur-3xl" />
          <div className="absolute -bottom-24 left-1/3 h-72 w-72 rounded-full bg-cyan-500/10 blur-3xl" />

          <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

            <div className="max-w-2xl">

              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 text-xs text-violet-300">
                <TrendingUp size={13} />
                Intelligence Analytics
              </div>

              <h2 className="text-2xl font-bold lg:text-3xl">
                NEXUS ONE Intelligence Overview
              </h2>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                Track AI usage, knowledge retrieval, document activity,
                conversations and system performance from one centralized
                analytics workspace.
              </p>

            </div>

            <div className="shrink-0 rounded-2xl border border-white/10 bg-black/20 px-5 py-4">

              <div className="flex items-center gap-3">
                <Activity size={21} className="text-emerald-400" />

                <div>
                  <div className="text-xs text-gray-500">
                    System Activity
                  </div>

                  <div className="mt-1 font-semibold text-emerald-400">
                    Operational
                  </div>
                </div>
              </div>

            </div>

          </div>
        </section>

        {/* METRICS */}
        <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                AI Queries
              </span>
              <Brain size={18} className="text-violet-400" />
            </div>

            <div className="mt-4 text-3xl font-bold">
              0
            </div>

            <div className="mt-2 flex items-center gap-1 text-xs text-gray-500">
              <TrendingUp size={13} />
              Questions processed
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                Documents
              </span>
              <FileText size={18} className="text-cyan-400" />
            </div>

            <div className="mt-4 text-3xl font-bold">
              0
            </div>

            <div className="mt-2 flex items-center gap-1 text-xs text-gray-500">
              <Database size={13} />
              Knowledge sources
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                Conversations
              </span>
              <History size={18} className="text-blue-400" />
            </div>

            <div className="mt-4 text-3xl font-bold">
              0
            </div>

            <div className="mt-2 flex items-center gap-1 text-xs text-gray-500">
              <MessageSquare size={13} />
              Saved conversations
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                System Health
              </span>
              <ShieldCheck size={18} className="text-emerald-400" />
            </div>

            <div className="mt-4 text-3xl font-bold text-emerald-400">
              100%
            </div>

            <div className="mt-2 flex items-center gap-1 text-xs text-emerald-400">
              <Activity size={13} />
              Operational status
            </div>
          </div>

        </section>

        {/* USAGE + AI PERFORMANCE */}
        <section className="mt-8 grid gap-6 lg:grid-cols-2">

          {/* USAGE */}
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">

            <div className="flex items-center justify-between">

              <div>
                <h2 className="font-semibold">
                  Usage Overview
                </h2>

                <p className="mt-1 text-xs text-gray-500">
                  Current workspace activity
                </p>
              </div>

              <BarChart3 size={20} className="text-gray-500" />

            </div>

            <div className="mt-7 space-y-6">

              {usage.map((item) => (
                <div key={item.label}>

                  <div className="mb-2 flex items-center justify-between">

                    <span className="text-sm text-gray-400">
                      {item.label}
                    </span>

                    <span className="text-sm font-medium">
                      {item.value}
                    </span>

                  </div>

                  <div className="h-2 overflow-hidden rounded-full bg-white/5">
                    <div
                      className="h-full rounded-full bg-violet-500 transition-all"
                      style={{ width: `${item.percentage}%` }}
                    />
                  </div>

                </div>
              ))}

            </div>
          </div>

          {/* AI PERFORMANCE */}
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">

            <div className="flex items-center justify-between">

              <div>
                <h2 className="font-semibold">
                  AI Performance
                </h2>

                <p className="mt-1 text-xs text-gray-500">
                  NEXUS AI engine metrics
                </p>
              </div>

              <Zap size={20} className="text-yellow-400" />

            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">

              <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
                <div className="text-xs text-gray-500">
                  AI Engine
                </div>

                <div className="mt-2 font-semibold">
                  NEXUS AI
                </div>

                <div className="mt-2 text-xs text-emerald-400">
                  Operational
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
                <div className="text-xs text-gray-500">
                  Retrieval
                </div>

                <div className="mt-2 font-semibold">
                  RAG
                </div>

                <div className="mt-2 text-xs text-emerald-400">
                  Available
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
                <div className="text-xs text-gray-500">
                  Knowledge Search
                </div>

                <div className="mt-2 font-semibold">
                  FAISS
                </div>

                <div className="mt-2 text-xs text-emerald-400">
                  Ready
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
                <div className="text-xs text-gray-500">
                  Response Status
                </div>

                <div className="mt-2 font-semibold">
                  Ready
                </div>

                <div className="mt-2 text-xs text-emerald-400">
                  Operational
                </div>
              </div>

            </div>
          </div>

        </section>

        {/* KNOWLEDGE ANALYTICS */}
        <section className="mt-6 rounded-3xl border border-white/10 bg-white/[0.03] p-6">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5">
              <Search size={19} />
            </div>

            <div>
              <h2 className="font-semibold">
                Knowledge Retrieval
              </h2>

              <p className="text-xs text-gray-500">
                Document and knowledge-base intelligence
              </p>
            </div>

          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                Indexed Documents
              </div>
              <div className="mt-3 text-2xl font-bold">
                0
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                Vector Search
              </div>
              <div className="mt-3 text-2xl font-bold">
                Ready
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                Retrieval Engine
              </div>
              <div className="mt-3 text-2xl font-bold">
                FAISS
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                Knowledge Status
              </div>
              <div className="mt-3 text-2xl font-bold text-emerald-400">
                Ready
              </div>
            </div>

          </div>
        </section>

        {/* RECENT ACTIVITY */}
        <section className="mt-6 rounded-3xl border border-white/10 bg-white/[0.03]">

          <div className="flex items-center justify-between border-b border-white/10 p-6">

            <div>
              <h2 className="font-semibold">
                Recent Activity
              </h2>

              <p className="mt-1 text-xs text-gray-500">
                Latest NEXUS ONE workspace events
              </p>
            </div>

            <Clock3 size={19} className="text-gray-500" />

          </div>

          <div className="divide-y divide-white/10">

            {activity.map((item) => {
              const Icon = item.icon;

              return (
                <div
                  key={item.title}
                  className="flex items-center justify-between gap-4 p-5 hover:bg-white/[0.02]"
                >

                  <div className="flex items-center gap-4">

                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5">
                      <Icon size={18} className="text-gray-300" />
                    </div>

                    <div>
                      <div className="text-sm font-medium">
                        {item.title}
                      </div>

                      <div className="mt-1 text-xs text-gray-500">
                        {item.description}
                      </div>
                    </div>

                  </div>

                  <span className="text-xs text-gray-600">
                    {item.time}
                  </span>

                </div>
              );
            })}

          </div>
        </section>

        {/* FOOTER */}
        <footer className="mt-10 border-t border-white/10 pt-6 text-center text-xs text-gray-600">
          NEXUS ONE — AI Powered Enterprise Intelligence Platform
        </footer>

      </div>
    </main>
  );
}
