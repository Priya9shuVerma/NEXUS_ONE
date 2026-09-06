"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Brain, Mail, Loader2 } from "lucide-react";
import api from "@/services/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [resetToken, setResetToken] = useState("");

  const handleSubmit = async () => {
    setMessage("");
    setError("");
    setResetToken("");

    const cleanEmail = email.trim();

    if (!cleanEmail) {
      setError("Please enter your email address.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/auth/forgot-password", {
        email: cleanEmail,
      });

      setMessage(
        response.data?.message ||
          "If the account exists, a password reset request has been created."
      );

      if (response.data?.reset_token) {
        setResetToken(response.data.reset_token);
      }
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Unable to create password reset request."
      );
    } finally {
      setLoading(false);
    }
  };

  const openResetPage = () => {
    if (!resetToken) return;

    window.location.href =
      `/reset-password?token=${encodeURIComponent(resetToken)}`;
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#05070b] px-4 text-white">
      <div className="w-full max-w-md">

        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-pink-500 to-violet-600">
            <Brain size={28} />
          </div>

          <h1 className="text-2xl font-bold">
            Forgot Password?
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Enter your email and we'll help you reset your password.
          </p>
        </div>

        <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl">

          <label className="mb-2 block text-sm text-gray-300">
            Email Address
          </label>

          <div className="relative">
            <Mail
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
            />

            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSubmit();
                }
              }}
              placeholder="you@example.com"
              disabled={loading}
              className="w-full rounded-xl border border-white/10 bg-black/20 py-3 pl-11 pr-4 text-sm outline-none transition placeholder:text-gray-600 focus:border-pink-500/50 disabled:opacity-50"
            />
          </div>

          {error && (
            <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400">
              {error}
            </div>
          )}

          {message && (
            <div className="mt-4 rounded-xl border border-green-500/20 bg-green-500/10 p-3 text-sm text-green-400">
              {message}
            </div>
          )}

          {resetToken && (
            <div className="mt-4 rounded-xl border border-pink-500/20 bg-pink-500/10 p-4">
              <p className="mb-2 text-xs text-gray-400">
                Development reset token
              </p>

              <div className="break-all rounded-lg bg-black/30 p-3 text-xs text-pink-300">
                {resetToken}
              </div>

              <button
                type="button"
                onClick={openResetPage}
                className="mt-3 w-full rounded-xl bg-pink-500 py-3 text-sm font-semibold text-white transition hover:bg-pink-400"
              >
                Continue to Reset Password
              </button>
            </div>
          )}

          {!resetToken && (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-white py-3 text-sm font-semibold text-black transition hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Sending...
                </>
              ) : (
                "Send Reset Link"
              )}
            </button>
          )}

          <Link
            href="/login"
            className="mt-5 flex items-center justify-center gap-2 text-sm text-gray-400 hover:text-white"
          >
            <ArrowLeft size={16} />
            Back to Login
          </Link>

        </div>

        <p className="mt-6 text-center text-xs text-gray-600">
          NEXUS ONE Security
        </p>

      </div>
    </main>
  );
}
