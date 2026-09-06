"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Brain,
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { registerUser } from "@/services/auth";

export default function RegisterPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");

    if (!username || !email || !password) {
      setError("Please complete all fields.");
      return;
    }

    try {
      setLoading(true);

      const response = await registerUser({
        username,
        email,
        password,
      });

      console.log(response);

      router.push("/login");
    } catch (error) {
      console.error("Register Error:", error);
      setError("Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative flex min-h-screen overflow-hidden bg-[#05070b] text-white">

      {/* Background effects */}
      <div className="pointer-events-none absolute -left-40 -top-40 h-96 w-96 rounded-full bg-pink-500/10 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-40 -right-40 h-96 w-96 rounded-full bg-violet-600/10 blur-3xl" />

      {/* Branding */}
      <section className="relative hidden flex-1 items-center justify-center border-r border-white/10 px-12 lg:flex">

        <div className="max-w-xl">

          <div className="mb-8 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-pink-500 to-violet-600 shadow-xl shadow-pink-500/20">
              <Brain size={25} />
            </div>

            <div>
              <div className="text-xl font-bold tracking-wide">
                NEXUS ONE
              </div>

              <div className="text-[10px] uppercase tracking-[0.28em] text-gray-500">
                Intelligence Platform
              </div>
            </div>
          </div>

          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-pink-500/20 bg-pink-500/10 px-3 py-1.5 text-xs text-pink-300">
            <Sparkles size={14} />
            AI Powered Workspace
          </div>

          <h1 className="text-5xl font-bold leading-tight">
            Build your
            <span className="block bg-gradient-to-r from-pink-400 to-violet-400 bg-clip-text text-transparent">
              intelligent workspace.
            </span>
          </h1>

          <p className="mt-6 max-w-lg text-base leading-7 text-gray-400">
            Create your NEXUS ONE account and access AI knowledge,
            documents, analytics, security and intelligent workflows
            from one centralized platform.
          </p>

          <div className="mt-8 flex items-center gap-3 text-sm text-gray-500">
            <ShieldCheck size={18} className="text-emerald-400" />
            Secure enterprise intelligence environment
          </div>

        </div>
      </section>

      {/* Register */}
      <section className="relative flex w-full items-center justify-center px-5 py-10 lg:w-[520px] lg:px-10">

        <div className="w-full max-w-md">

          {/* Mobile brand */}
          <div className="mb-8 flex items-center justify-center gap-3 lg:hidden">

            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-pink-500 to-violet-600">
              <Brain size={23} />
            </div>

            <div>
              <div className="font-bold">
                NEXUS ONE
              </div>

              <div className="text-[9px] uppercase tracking-[0.25em] text-gray-500">
                Intelligence Platform
              </div>
            </div>

          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-bold">
              Create your account
            </h2>

            <p className="mt-2 text-sm text-gray-500">
              Join NEXUS ONE and start building your intelligent workspace.
            </p>
          </div>

          <form
            onSubmit={handleRegister}
            className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl backdrop-blur-xl sm:p-8"
          >

            {/* Username */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-300">
                Username
              </label>

              <div className="relative">

                <User
                  size={18}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
                />

                <input
                  type="text"
                  placeholder="Your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-black/20 py-3.5 pl-11 pr-4 text-sm outline-none transition placeholder:text-gray-600 focus:border-pink-500/50 focus:bg-white/[0.04]"
                />

              </div>
            </div>

            {/* Email */}
            <div className="mt-5">

              <label className="mb-2 block text-sm font-medium text-gray-300">
                Email Address
              </label>

              <div className="relative">

                <Mail
                  size={18}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
                />

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-black/20 py-3.5 pl-11 pr-4 text-sm outline-none transition placeholder:text-gray-600 focus:border-pink-500/50 focus:bg-white/[0.04]"
                />

              </div>

            </div>

            {/* Password */}
            <div className="mt-5">

              <label className="mb-2 block text-sm font-medium text-gray-300">
                Password
              </label>

              <div className="relative">

                <Lock
                  size={18}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
                />

                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Create a password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-black/20 py-3.5 pl-11 pr-12 text-sm outline-none transition placeholder:text-gray-600 focus:border-pink-500/50 focus:bg-white/[0.04]"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg p-2 text-gray-500 hover:text-white"
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                >
                  {showPassword ? (
                    <EyeOff size={17} />
                  ) : (
                    <Eye size={17} />
                  )}
                </button>

              </div>

            </div>

            {/* Error */}
            {error && (
              <div className="mt-5 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                {error}
              </div>
            )}

            {/* Register */}
            <button
              type="submit"
              disabled={loading}
              className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-white py-3.5 text-sm font-semibold text-black transition hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Creating account..." : "Create account"}

              {!loading && <ArrowRight size={17} />}
            </button>

            {/* Login */}
            <div className="mt-6 text-center text-sm text-gray-500">

              Already have an account?{" "}

              <Link
                href="/login"
                className="font-medium text-pink-400 hover:text-pink-300"
              >
                Sign in
              </Link>

            </div>

          </form>

          <div className="mt-6 flex items-center justify-center gap-2 text-xs text-gray-600">
            <ShieldCheck size={14} />
            Protected by NEXUS ONE security
          </div>

        </div>
      </section>
    </main>
  );
}
