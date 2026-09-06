"use client";

import Link from "next/link";
import {
  ArrowLeft,
  Brain,
  FileText,
  Sparkles,
  Search,
  Languages,
  Lightbulb,
  BarChart3,
  ShieldCheck,
  WandSparkles,
  MessageSquareText,
} from "lucide-react";

const tools = [
  {
    name: "AI Summarizer",
    description: "Summarize long documents, articles and text into concise insights.",
    icon: FileText,
    status: "Ready",
  },
  {
    name: "Document Q&A",
    description: "Ask intelligent questions about your uploaded knowledge base.",
    icon: MessageSquareText,
    status: "Ready",
  },
  {
    name: "Text Generator",
    description: "Generate professional content, ideas, explanations and responses.",
    icon: WandSparkles,
    status: "Ready",
  },
  {
    name: "Document Analyzer",
    description: "Analyze documents and extract important information and patterns.",
    icon: Search,
    status: "Ready",
  },
  {
    name: "AI Translator",
    description: "Translate text between supported languages while preserving meaning.",
    icon: Languages,
    status: "Ready",
  },
  {
    name: "Idea Generator",
    description: "Generate project ideas, solutions, concepts and creative directions.",
    icon: Lightbulb,
    status: "Ready",
  },
  {
    name: "Data Analyzer",
    description: "Explore datasets, discover patterns and generate analytical insights.",
    icon: BarChart3,
    status: "Ready",
  },
  {
    name: "Security Assistant",
    description: "Use AI to analyze security concepts, risks and cybersecurity information.",
    icon: ShieldCheck,
    status: "Ready",
  },
];

export default function ToolsPage() {
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
              <span>AI Tools</span>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-pink-500/20 to-violet-500/20 ring-1 ring-white/10">
                <Sparkles size={27} className="text-pink-300" />
              </div>

              <div>
                <h1 className="text-3xl font-bold tracking-tight">
                  AI Tools
                </h1>

                <p className="mt-1 text-sm text-gray-500">
                  Intelligent tools powered by the NEXUS ONE AI engine.
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
        <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-pink-500/[0.08] via-white/[0.03] to-violet-500/[0.06] p-6 lg:p-8">

          <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-pink-500/10 blur-3xl" />
          <div className="absolute -bottom-24 left-1/3 h-72 w-72 rounded-full bg-violet-500/10 blur-3xl" />

          <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-pink-500/20 bg-pink-500/10 px-3 py-1 text-xs text-pink-300">
                <Brain size={13} />
                NEXUS AI Engine
              </div>

              <h2 className="text-2xl font-bold lg:text-3xl">
                One workspace. Multiple AI capabilities.
              </h2>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                Access intelligent tools for documents, content generation,
                analysis, translation, ideas and cybersecurity from a single
                NEXUS ONE workspace.
              </p>
            </div>

            <Link
              href="/ai"
              className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black transition hover:bg-gray-200"
            >
              <Brain size={17} />
              Open AI Assistant
            </Link>

          </div>
        </section>

        {/* TOOL STATS */}
        <section className="mt-6 grid gap-4 sm:grid-cols-3">

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="text-sm text-gray-400">
              Available Tools
            </div>

            <div className="mt-3 text-3xl font-bold">
              8
            </div>

            <p className="mt-1 text-xs text-gray-500">
              AI capabilities
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="text-sm text-gray-400">
              AI Engine
            </div>

            <div className="mt-3 text-3xl font-bold">
              NEXUS AI
            </div>

            <p className="mt-1 text-xs text-gray-500">
              Intelligence layer
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="text-sm text-gray-400">
              Workspace
            </div>

            <div className="mt-3 text-3xl font-bold text-emerald-400">
              Ready
            </div>

            <p className="mt-1 text-xs text-gray-500">
              Integration pending
            </p>
          </div>

        </section>

        {/* TOOLS */}
        <section className="mt-8">

          <div className="mb-5">
            <h2 className="text-xl font-semibold">
              Intelligence Tools
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Select an AI capability to start working.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

            {tools.map((tool) => {
              const Icon = tool.icon;

              return (
                <div
                  key={tool.name}
                  className="group rounded-2xl border border-white/10 bg-white/[0.03] p-5 transition duration-200 hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.06]"
                >

                  <div className="flex items-start justify-between">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/5 text-gray-300 transition group-hover:bg-white/10 group-hover:text-white">
                      <Icon size={21} />
                    </div>

                    <span className="rounded-full border border-emerald-500/20 bg-emerald-500/5 px-2.5 py-1 text-[10px] font-medium text-emerald-400">
                      {tool.status}
                    </span>

                  </div>

                  <h3 className="mt-5 font-semibold">
                    {tool.name}
                  </h3>

                  <p className="mt-2 min-h-[60px] text-xs leading-5 text-gray-500">
                    {tool.description}
                  </p>

                  <Link
                    href="/ai"
                    className="mt-5 inline-flex items-center gap-2 text-xs font-medium text-gray-400 transition hover:text-white"
                  >
                    Open tool
                    <span>→</span>
                  </Link>

                </div>
              );
            })}

          </div>
        </section>

        {/* QUICK ACTIONS */}
        <section className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-6">

          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <h2 className="font-semibold">
                Quick AI Actions
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Start directly from the main NEXUS ONE assistant.
              </p>
            </div>

            <div className="flex flex-wrap gap-3">

              <Link
                href="/ai"
                className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm hover:bg-white/10"
              >
                <MessageSquareText size={16} />
                Ask AI
              </Link>

              <Link
                href="/dashboard/documents"
                className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm hover:bg-white/10"
              >
                <FileText size={16} />
                Documents
              </Link>

              <Link
                href="/dashboard/security"
                className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm hover:bg-white/10"
              >
                <ShieldCheck size={16} />
                Security
              </Link>

            </div>

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
