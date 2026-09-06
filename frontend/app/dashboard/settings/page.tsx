"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  ArrowLeft,
  Brain,
  Save,
  Lock,
  LogOut,
  Loader2,
  User,
} from "lucide-react";

import {
  getProfile,
  updateProfile,
  changePassword,
  logoutUser,
} from "@/services/auth";

export default function Page() {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [changingPassword, setChangingPassword] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [profile, setProfile] = useState({
    username: "",
    email: "",
    full_name: "",
    phone: "",
    bio: "",
    profile_image: "",
  });

  const [passwords, setPasswords] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });

  // ----------------------------------------------------------
  // Load profile
  // ----------------------------------------------------------

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");

        if (!token) {
          router.replace("/login");
          return;
        }

        const data = await getProfile();

        setProfile({
          username: data.username || "",
          email: data.email || "",
          full_name: data.full_name || "",
          phone: data.phone || "",
          bio: data.bio || "",
          profile_image: data.profile_image || "",
        });
      } catch (err: any) {
        if (err?.response?.status === 401) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          router.replace("/login");
          return;
        }

        setError(
          err?.response?.data?.detail ||
            "Unable to load profile."
        );
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, [router]);

  // ----------------------------------------------------------
  // Update profile
  // ----------------------------------------------------------

  const handleProfileSave = async () => {
    setMessage("");
    setError("");

    try {
      setSaving(true);

      const data = await updateProfile({
        full_name: profile.full_name,
        phone: profile.phone,
        bio: profile.bio,
        profile_image: profile.profile_image,
      });

      setMessage(
        data?.message ||
          "Profile updated successfully."
      );
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Unable to update profile."
      );
    } finally {
      setSaving(false);
    }
  };

  // ----------------------------------------------------------
  // Change password
  // ----------------------------------------------------------

  const handlePasswordChange = async () => {
    setMessage("");
    setError("");

    if (!passwords.old_password) {
      setError("Enter your current password.");
      return;
    }

    if (!passwords.new_password) {
      setError("Enter your new password.");
      return;
    }

    if (passwords.new_password.length < 8) {
      setError(
        "New password must be at least 8 characters."
      );
      return;
    }

    if (
      passwords.new_password !==
      passwords.confirm_password
    ) {
      setError("New passwords do not match.");
      return;
    }

    try {
      setChangingPassword(true);

      const data = await changePassword({
        old_password: passwords.old_password,
        new_password: passwords.new_password,
      });

      setMessage(
        data?.message ||
          "Password changed successfully."
      );

      setPasswords({
        old_password: "",
        new_password: "",
        confirm_password: "",
      });
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Unable to change password."
      );
    } finally {
      setChangingPassword(false);
    }
  };

  // ----------------------------------------------------------
  // Logout
  // ----------------------------------------------------------

  const handleLogout = async () => {
    try {
      setLoggingOut(true);
      await logoutUser();
    } finally {
      router.replace("/login");
    }
  };

  // ----------------------------------------------------------
  // Loading
  // ----------------------------------------------------------

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#05070b] text-white">
        <Loader2
          size={28}
          className="animate-spin text-pink-400"
        />
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#05070b] px-5 py-8 text-white lg:px-10">
      <div className="mx-auto max-w-5xl">

        {/* Header */}

        <div className="mb-8 flex items-center justify-between">

          <div>
            <div className="mb-2 flex items-center gap-2 text-xs text-gray-500">
              <Link
                href="/dashboard"
                className="hover:text-white"
              >
                Dashboard
              </Link>

              <span>/</span>

              <span>Profile / Settings</span>
            </div>

            <h1 className="text-3xl font-bold">
              Profile / Settings
            </h1>

            <p className="mt-2 text-sm text-gray-500">
              Manage your NEXUS ONE account and security.
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

        {/* Messages */}

        {error && (
          <div className="mb-5 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
            {error}
          </div>
        )}

        {message && (
          <div className="mb-5 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-4 text-sm text-emerald-400">
            {message}
          </div>
        )}

        {/* Account */}

        <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">

          <div className="mb-6 flex items-center gap-4">

            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-pink-500 to-violet-600">
              <User size={25} />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                Account Profile
              </h2>

              <p className="text-sm text-gray-500">
                Update your personal information.
              </p>
            </div>

          </div>

          <div className="grid gap-5 md:grid-cols-2">

            <div>
              <label className="mb-2 block text-sm text-gray-400">
                Username
              </label>

              <input
                value={profile.username}
                disabled
                className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm text-gray-500 outline-none"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-gray-400">
                Email
              </label>

              <input
                value={profile.email}
                disabled
                className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm text-gray-500 outline-none"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-gray-400">
                Full Name
              </label>

              <input
                value={profile.full_name}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    full_name: e.target.value,
                  })
                }
                placeholder="Your full name"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none focus:border-pink-500/50"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-gray-400">
                Phone
              </label>

              <input
                value={profile.phone}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    phone: e.target.value,
                  })
                }
                placeholder="Phone number"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none focus:border-pink-500/50"
              />
            </div>

          </div>

          <div className="mt-5">

            <label className="mb-2 block text-sm text-gray-400">
              Bio
            </label>

            <textarea
              value={profile.bio}
              onChange={(e) =>
                setProfile({
                  ...profile,
                  bio: e.target.value,
                })
              }
              rows={4}
              placeholder="Tell us something about yourself..."
              className="w-full resize-none rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none focus:border-pink-500/50"
            />

          </div>

          <button
            type="button"
            onClick={handleProfileSave}
            disabled={saving}
            className="mt-5 flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black hover:bg-gray-200 disabled:opacity-60"
          >
            {saving ? (
              <Loader2
                size={16}
                className="animate-spin"
              />
            ) : (
              <Save size={16} />
            )}

            {saving ? "Saving..." : "Save Profile"}
          </button>

        </section>

        {/* Password */}

        <section className="mt-6 rounded-3xl border border-white/10 bg-white/[0.03] p-6">

          <div className="mb-6 flex items-center gap-4">

            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-white/5">
              <Lock size={24} />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                Change Password
              </h2>

              <p className="text-sm text-gray-500">
                Keep your account secure with a strong password.
              </p>
            </div>

          </div>

          <div className="grid gap-5 md:grid-cols-3">

            <input
              type="password"
              value={passwords.old_password}
              onChange={(e) =>
                setPasswords({
                  ...passwords,
                  old_password: e.target.value,
                })
              }
              placeholder="Current password"
              className="rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm outline-none focus:border-pink-500/50"
            />

            <input
              type="password"
              value={passwords.new_password}
              onChange={(e) =>
                setPasswords({
                  ...passwords,
                  new_password: e.target.value,
                })
              }
              placeholder="New password"
              className="rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm outline-none focus:border-pink-500/50"
            />

            <input
              type="password"
              value={passwords.confirm_password}
              onChange={(e) =>
                setPasswords({
                  ...passwords,
                  confirm_password: e.target.value,
                })
              }
              placeholder="Confirm password"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handlePasswordChange();
                }
              }}
              className="rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm outline-none focus:border-pink-500/50"
            />

          </div>

          <button
            type="button"
            onClick={handlePasswordChange}
            disabled={changingPassword}
            className="mt-5 flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-semibold hover:bg-white/10 disabled:opacity-60"
          >
            {changingPassword ? (
              <Loader2
                size={16}
                className="animate-spin"
              />
            ) : (
              <Lock size={16} />
            )}

            {changingPassword
              ? "Changing..."
              : "Change Password"}
          </button>

        </section>

        {/* Logout */}

        <section className="mt-6 rounded-3xl border border-red-500/10 bg-red-500/[0.03] p-6">

          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <h2 className="text-lg font-semibold">
                Sign Out
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Sign out from this NEXUS ONE session.
              </p>
            </div>

            <button
              type="button"
              onClick={handleLogout}
              disabled={loggingOut}
              className="flex items-center justify-center gap-2 rounded-xl border border-red-500/20 bg-red-500/10 px-5 py-3 text-sm font-semibold text-red-400 hover:bg-red-500/20 disabled:opacity-60"
            >
              {loggingOut ? (
                <Loader2
                  size={16}
                  className="animate-spin"
                />
              ) : (
                <LogOut size={16} />
              )}

              {loggingOut ? "Signing out..." : "Logout"}
            </button>

          </div>

        </section>

        <footer className="mt-10 border-t border-white/10 pt-6 text-center text-xs text-gray-600">
          NEXUS ONE — AI Powered Enterprise Intelligence Platform
        </footer>

      </div>
    </main>
  );
}
