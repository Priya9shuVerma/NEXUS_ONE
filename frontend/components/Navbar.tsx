"use client";

import { Bell, Search, UserCircle } from "lucide-react";

export default function Navbar() {
  return (
    <header className="h-16 bg-zinc-900 border-b border-zinc-800 flex items-center justify-between px-8">

      <div className="relative">

        <Search
          size={18}
          className="absolute left-3 top-3 text-gray-400"
        />

        <input
          type="text"
          placeholder="Search..."
          className="bg-zinc-800 rounded-lg pl-10 pr-4 py-2 text-white outline-none w-72"
        />

      </div>

      <div className="flex items-center gap-6">

        <Bell
          className="text-gray-300 hover:text-white cursor-pointer"
          size={22}
        />

        <div className="flex items-center gap-2">

          <UserCircle
            size={34}
            className="text-blue-400"
          />

          <div>

            <p className="text-white font-semibold">
              Priyanshu
            </p>

            <p className="text-xs text-gray-400">
              Administrator
            </p>

          </div>

        </div>

      </div>

    </header>
  );
}
