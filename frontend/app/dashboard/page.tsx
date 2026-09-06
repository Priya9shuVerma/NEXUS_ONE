"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Brain,
  FileText,
  History,
  Wrench,
  Shield,
  Cloud,
  BarChart3,
  Settings,
  LogOut,
  User,
  Menu,
  X,
} from "lucide-react";
import { useState } from "react";

const navigation = [
  {
    name: "Overview",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "AI Knowledge Assistant",
    href: "/ai",
    icon: Brain,
  },
  {
    name: "Documents",
    href: "/dashboard/documents",
    icon: FileText,
  },
  {
    name: "Chat History",
    href: "/dashboard/history",
    icon: History,
  },
  {
    name: "AI Tools",
    href: "/dashboard/tools",
    icon: Wrench,
  },
  {
    name: "Security",
    href: "/dashboard/security",
    icon: Shield,
  },
  {
    name: "Cloud Security",
    href: "/dashboard/cloud",
    icon: Cloud,
  },
  {
    name: "Analytics",
    href: "/dashboard/analytics",
    icon: BarChart3,
  },
  {
    name: "Profile / Settings",
    href: "/dashboard/settings",
    icon: Settings,
  },
];

export default function DashboardPage() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#05070b] text-white">
      <div className="flex min-h-screen">

        {/* SIDEBAR */}
        <aside
          className={`
            fixed inset-y-0 left-0 z-50 w-72
            border-r border-white/10 bg-[#080b12]
            transition-transform duration-300
            lg:static lg:translate-x-0
            ${mobileOpen ? "translate-x-0" : "-translate-x-full"}
          `}
        >
          <div className="flex h-full flex-col">

            {/* BRAND */}
            <div className="flex h-20 items-center justify-between border-b border-white/10 px-6">
              <Link href="/dashboard" className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-pink-500 to-violet-600 shadow-lg shadow-pink-500/20">
                  <Brain size={22} />
                </div>

                <div>
                  <div className="text-lg font-bold tracking-wide">
                    NEXUS ONE
                  </div>
                  <div className="text-[10px] uppercase tracking-[0.25em] text-gray-500">
                    Intelligence Platform
                  </div>
                </div>
              </Link>

              <button
                onClick={() => setMobileOpen(false)}
                className="rounded-lg p-2 text-gray-400 hover:bg-white/5 hover:text-white lg:hidden"
              >
                <X size={20} />
              </button>
            </div>

            {/* NAVIGATION */}
            <nav className="flex-1 space-y-1 overflow-y-auto p-4">

              <div className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-gray-500">
                Workspace
              </div>

              {navigation.map((item) => {
                const Icon = item.icon;

                const active =
                  item.href === "/dashboard"
                    ? pathname === "/dashboard"
                    : pathname.startsWith(item.href);

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileOpen(false)}
                    className={`
                      flex items-center gap-3 rounded-xl px-4 py-3
                      text-sm transition-all
                      ${
                        active
                          ? "bg-white/10 text-white shadow-inner"
                          : "text-gray-400 hover:bg-white/5 hover:text-white"
                      }
                    `}
                  >
                    <Icon size={19} />

                    <span>{item.name}</span>

                    {active && (
                      <span className="ml-auto h-2 w-2 rounded-full bg-pink-500 shadow-lg shadow-pink-500/50" />
                    )}
                  </Link>
                );
              })}
            </nav>

            {/* USER / LOGOUT */}
            <div className="border-t border-white/10 p-4">

              <Link
                href="/dashboard/settings"
                className="mb-2 flex items-center gap-3 rounded-xl p-3 hover:bg-white/5"
              >
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white/10">
                  <User size={17} />
                </div>

                <div className="min-w-0">
                  <div className="truncate text-sm font-medium">
                    NEXUS User
                  </div>
                  <div className="text-xs text-gray-500">
                    Account Settings
                  </div>
                </div>
              </Link>

              <Link
                href="/login"
                className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm text-gray-400 hover:bg-red-500/10 hover:text-red-400"
              >
                <LogOut size={18} />
                Logout
              </Link>
            </div>
          </div>
        </aside>

        {/* MOBILE OVERLAY */}
        {mobileOpen && (
          <button
            aria-label="Close menu"
            onClick={() => setMobileOpen(false)}
            className="fixed inset-0 z-40 bg-black/60 lg:hidden"
          />
        )}

        {/* MAIN */}
        <main className="min-w-0 flex-1">

          {/* TOPBAR */}
          <header className="flex h-20 items-center justify-between border-b border-white/10 bg-[#070a10]/90 px-5 backdrop-blur-xl lg:px-8">

            <div className="flex items-center gap-3">
              <button
                onClick={() => setMobileOpen(true)}
                className="rounded-xl border border-white/10 p-2 text-gray-300 hover:bg-white/5 lg:hidden"
              >
                <Menu size={20} />
              </button>

              <div>
                <h1 className="text-lg font-semibold">
                  Dashboard
                </h1>
                <p className="hidden text-xs text-gray-500 sm:block">
                  NEXUS ONE Intelligence Workspace
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="hidden items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/5 px-3 py-1.5 text-xs text-emerald-400 sm:flex">
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
                System Online
              </div>

              <Link
                href="/dashboard/settings"
                className="flex h-9 w-9 items-center justify-center rounded-full border border-white/10 bg-white/5 hover:bg-white/10"
              >
                <User size={17} />
              </Link>
            </div>
          </header>

          {/* CONTENT */}
          <div className="p-5 lg:p-8">

            {/* HERO */}
            <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/[0.07] to-white/[0.02] p-6 lg:p-8">

              <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-pink-500/10 blur-3xl" />
              <div className="absolute -bottom-20 left-1/3 h-64 w-64 rounded-full bg-violet-500/10 blur-3xl" />

              <div className="relative">
                <div className="mb-3 inline-flex rounded-full border border-pink-500/20 bg-pink-500/10 px-3 py-1 text-xs text-pink-300">
                  AI Powered Workspace
                </div>

                <h2 className="text-3xl font-bold tracking-tight lg:text-4xl">
                  Welcome to NEXUS ONE
                </h2>

                <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-400">
                  Your centralized AI intelligence platform for documents,
                  knowledge discovery, analytics, security and intelligent
                  workflows.
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    href="/ai"
                    className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black transition hover:bg-gray-200"
                  >
                    <Brain size={17} />
                    Open AI Assistant
                  </Link>

                  <Link
                    href="/dashboard/documents"
                    className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-medium text-white hover:bg-white/10"
                  >
                    <FileText size={17} />
                    Documents
                  </Link>
                </div>
              </div>
            </section>

            {/* STATS */}
            <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">
                    Documents
                  </span>
                  <FileText size={18} className="text-gray-400" />
                </div>
                <div className="mt-4 text-3xl font-bold">0</div>
                <div className="mt-1 text-xs text-gray-500">
                  Knowledge sources
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">
                    AI Queries
                  </span>
                  <Brain size={18} className="text-gray-400" />
                </div>
                <div className="mt-4 text-3xl font-bold">0</div>
                <div className="mt-1 text-xs text-gray-500">
                  Questions processed
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">
                    Conversations
                  </span>
                  <History size={18} className="text-gray-400" />
                </div>
                <div className="mt-4 text-3xl font-bold">0</div>
                <div className="mt-1 text-xs text-gray-500">
                  Saved conversations
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">
                    Security
                  </span>
                  <Shield size={18} className="text-emerald-400" />
                </div>
                <div className="mt-4 text-3xl font-bold">
                  Active
                </div>
                <div className="mt-1 text-xs text-emerald-400">
                  Protected workspace
                </div>
              </div>

            </section>

            {/* MODULES */}
            <section className="mt-8">

              <div className="mb-4">
                <h3 className="text-xl font-semibold">
                  Intelligence Modules
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  Access every NEXUS ONE capability from one workspace.
                </p>
              </div>

              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

                {navigation
                  .filter((item) => item.href !== "/dashboard")
                  .map((item) => {
                    const Icon = item.icon;

                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        className="group rounded-2xl border border-white/10 bg-white/[0.03] p-5 transition hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.06]"
                      >
                        <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl bg-white/5 text-gray-300 transition group-hover:bg-white/10 group-hover:text-white">
                          <Icon size={21} />
                        </div>

                        <h4 className="font-medium">
                          {item.name}
                        </h4>

                        <p className="mt-2 text-xs leading-5 text-gray-500">
                          Explore the {item.name.toLowerCase()} module.
                        </p>
                      </Link>
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
      </div>
    </div>
  );
}


