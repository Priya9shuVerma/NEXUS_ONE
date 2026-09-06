"use client";

import Link from "next/link";
import {
  ArrowLeft,
  Brain,
  FileText,
  History,
  Wrench,
  Shield,
  BarChart3,
  Settings,
} from "lucide-react";

export default function Page() {
  return (
    <main className="min-h-screen bg-[#05070b] px-5 py-8 text-white lg:px-10">

      <div className="mx-auto max-w-7xl">

        <div className="mb-8 flex items-center justify-between">

          <div>
            <div className="mb-2 flex items-center gap-2 text-xs text-gray-500">
              <Link href="/dashboard" className="hover:text-white">
                Dashboard
              </Link>
              <span>/</span>
              <span>Overview</span>
            </div>

            <h1 className="text-3xl font-bold">
              Overview
            </h1>

            <p className="mt-2 text-sm text-gray-500">
              NEXUS ONE intelligence workspace
            </p>
          </div>

          <Link
            href="/dashboard"
            className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-gray-300 hover:bg-white/10 hover:text-white"
          >
            <ArrowLeft size={17} />
            Dashboard
          </Link>

        </div>

        <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-8">

          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
            <Brain size={28} />
          </div>

          <h2 className="mt-6 text-2xl font-semibold">
            Overview Module
          </h2>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-500">
            This module is part of the NEXUS ONE enterprise intelligence
            platform. The complete functionality will be connected during
            the integration and testing phase.
          </p>

          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                Status
              </div>
              <div className="mt-2 text-lg font-semibold">
                Ready
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                Integration
              </div>
              <div className="mt-2 text-lg font-semibold">
                Pending
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                AI Engine
              </div>
              <div className="mt-2 text-lg font-semibold">
                NEXUS AI
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <div className="text-xs text-gray-500">
                Security
              </div>
              <div className="mt-2 text-lg font-semibold text-emerald-400">
                Protected
              </div>
            </div>

          </div>

        </section>

        <footer className="mt-10 border-t border-white/10 pt-6 text-center text-xs text-gray-600">
          NEXUS ONE — AI Powered Enterprise Intelligence Platform
        </footer>

      </div>

    </main>
  );
}
