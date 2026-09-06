"use client";

import Link from "next/link";
import {
  ArrowLeft,
  Shield,
  ShieldCheck,
  Lock,
  KeyRound,
  UserCheck,
  Activity,
  AlertTriangle,
  CheckCircle2,
  Eye,
  Server,
  Fingerprint,
  Clock3,
  Settings,
} from "lucide-react";

const securityItems = [
  {
    title: "Authentication",
    description: "User authentication and protected account access.",
    icon: UserCheck,
    status: "Protected",
  },
  {
    title: "JWT Sessions",
    description: "Token-based session authentication for API access.",
    icon: KeyRound,
    status: "Active",
  },
  {
    title: "Data Protection",
    description: "Application data protection and secure communication.",
    icon: Lock,
    status: "Protected",
  },
  {
    title: "Access Control",
    description: "Authenticated access to protected NEXUS ONE resources.",
    icon: Fingerprint,
    status: "Active",
  },
];

export default function SecurityPage() {
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
              <span>Security</span>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-500/10 ring-1 ring-emerald-500/20">
                <ShieldCheck size={28} className="text-emerald-400" />
              </div>

              <div>
                <h1 className="text-3xl font-bold tracking-tight">
                  Security
                </h1>

                <p className="mt-1 text-sm text-gray-500">
                  Monitor and manage NEXUS ONE security controls.
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

        {/* SECURITY HERO */}
        <section className="relative overflow-hidden rounded-3xl border border-emerald-500/20 bg-gradient-to-br from-emerald-500/[0.08] via-white/[0.03] to-cyan-500/[0.05] p-6 lg:p-8">

          <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-emerald-500/10 blur-3xl" />
          <div className="absolute -bottom-24 left-1/3 h-72 w-72 rounded-full bg-cyan-500/10 blur-3xl" />

          <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-300">
                <ShieldCheck size={13} />
                Security Status
              </div>

              <h2 className="text-2xl font-bold lg:text-3xl">
                NEXUS ONE workspace is protected
              </h2>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                Authentication, access control and application security
                controls are organized in one centralized security workspace.
              </p>
            </div>

            <div className="flex shrink-0 items-center gap-3 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 px-5 py-4">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-500/10">
                <Shield size={23} className="text-emerald-400" />
              </div>

              <div>
                <div className="text-xs text-gray-500">
                  Overall Status
                </div>
                <div className="mt-1 font-semibold text-emerald-400">
                  Protected
                </div>
              </div>
            </div>

          </div>
        </section>

        {/* SECURITY METRICS */}
        <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                Authentication
              </span>
              <UserCheck size={18} className="text-emerald-400" />
            </div>

            <div className="mt-4 text-2xl font-bold">
              Active
            </div>

            <p className="mt-1 text-xs text-gray-500">
              Protected authentication
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                Sessions
              </span>
              <KeyRound size={18} className="text-emerald-400" />
            </div>

            <div className="mt-4 text-2xl font-bold">
              JWT
            </div>

            <p className="mt-1 text-xs text-gray-500">
              Token based access
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                Threat Alerts
              </span>
              <AlertTriangle size={18} className="text-gray-500" />
            </div>

            <div className="mt-4 text-2xl font-bold">
              0
            </div>

            <p className="mt-1 text-xs text-gray-500">
              Active alerts
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">
                System
              </span>
              <Activity size={18} className="text-emerald-400" />
            </div>

            <div className="mt-4 text-2xl font-bold text-emerald-400">
              Secure
            </div>

            <p className="mt-1 text-xs text-gray-500">
              Workspace status
            </p>
          </div>

        </section>

        {/* SECURITY CONTROLS */}
        <section className="mt-8">

          <div className="mb-5">
            <h2 className="text-xl font-semibold">
              Security Controls
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Core security mechanisms available in NEXUS ONE.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2">

            {securityItems.map((item) => {
              const Icon = item.icon;

              return (
                <div
                  key={item.title}
                  className="group rounded-2xl border border-white/10 bg-white/[0.03] p-5 transition hover:border-white/20 hover:bg-white/[0.05]"
                >
                  <div className="flex items-start justify-between">

                    <div className="flex items-center gap-4">
                      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/5 text-gray-300 group-hover:bg-white/10 group-hover:text-white">
                        <Icon size={21} />
                      </div>

                      <div>
                        <h3 className="font-semibold">
                          {item.title}
                        </h3>

                        <p className="mt-1 text-xs text-gray-500">
                          {item.description}
                        </p>
                      </div>
                    </div>

                    <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/20 bg-emerald-500/5 px-2.5 py-1 text-[10px] text-emerald-400">
                      <CheckCircle2 size={12} />
                      {item.status}
                    </span>

                  </div>
                </div>
              );
            })}

          </div>
        </section>

        {/* ACTIVITY + ALERTS */}
        <section className="mt-8 grid gap-4 lg:grid-cols-2">

          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">

            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5">
                <Activity size={19} />
              </div>

              <div>
                <h2 className="font-semibold">
                  Security Activity
                </h2>

                <p className="text-xs text-gray-500">
                  Recent security events
                </p>
              </div>
            </div>

            <div className="mt-6 space-y-4">

              <div className="flex items-center justify-between border-b border-white/5 pb-4">
                <div className="flex items-center gap-3">
                  <CheckCircle2 size={16} className="text-emerald-400" />
                  <span className="text-sm text-gray-300">
                    Authentication system
                  </span>
                </div>

                <span className="text-xs text-gray-600">
                  Active
                </span>
              </div>

              <div className="flex items-center justify-between border-b border-white/5 pb-4">
                <div className="flex items-center gap-3">
                  <CheckCircle2 size={16} className="text-emerald-400" />
                  <span className="text-sm text-gray-300">
                    API access protection
                  </span>
                </div>

                <span className="text-xs text-gray-600">
                  Active
                </span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Clock3 size={16} className="text-gray-500" />
                  <span className="text-sm text-gray-300">
                    Security monitoring
                  </span>
                </div>

                <span className="text-xs text-gray-600">
                  Ready
                </span>
              </div>

            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">

            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5">
                <AlertTriangle size={19} />
              </div>

              <div>
                <h2 className="font-semibold">
                  Security Alerts
                </h2>

                <p className="text-xs text-gray-500">
                  Workspace security notifications
                </p>
              </div>
            </div>

            <div className="mt-6 rounded-2xl border border-emerald-500/10 bg-emerald-500/5 p-5">

              <div className="flex items-center gap-3">
                <CheckCircle2 size={21} className="text-emerald-400" />

                <div>
                  <div className="font-medium">
                    No active security alerts
                  </div>

                  <p className="mt-1 text-xs text-gray-500">
                    There are currently no alerts displayed in the security
                    workspace.
                  </p>
                </div>
              </div>

            </div>

            <Link
              href="/dashboard/settings"
              className="mt-5 inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white"
            >
              <Settings size={16} />
              Security Settings
              <span>→</span>
            </Link>

          </div>

        </section>

        {/* INFRASTRUCTURE */}
        <section className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-6">

          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5">
              <Server size={19} />
            </div>

            <div>
              <h2 className="font-semibold">
                Security Infrastructure
              </h2>

              <p className="text-xs text-gray-500">
                NEXUS ONE application protection layer
              </p>
            </div>
          </div>

          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">

            {[
              "Authentication",
              "Authorization",
              "Session Security",
              "API Protection",
            ].map((item) => (
              <div
                key={item}
                className="flex items-center gap-3 rounded-xl border border-white/10 bg-black/20 p-4"
              >
                <ShieldCheck
                  size={17}
                  className="text-emerald-400"
                />

                <span className="text-sm text-gray-300">
                  {item}
                </span>
              </div>
            ))}

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
