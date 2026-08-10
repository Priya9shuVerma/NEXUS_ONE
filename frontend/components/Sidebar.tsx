"use client";

import {
  LayoutDashboard,
  BrainCircuit,
  Shield,
  Users,
  Settings,
} from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-zinc-950 border-r border-zinc-800 text-white p-6">

      <h1 className="text-3xl font-bold text-blue-500 mb-10">
        NEXUS ONE
      </h1>

      <nav className="space-y-6">

        <div className="flex items-center gap-3 hover:text-blue-400 cursor-pointer">
          <LayoutDashboard size={20}/>
          <span>Dashboard</span>
        </div>

        <div className="flex items-center gap-3 hover:text-blue-400 cursor-pointer">
          <BrainCircuit size={20}/>
          <span>AI Assistant</span>
        </div>

        <div className="flex items-center gap-3 hover:text-blue-400 cursor-pointer">
          <Shield size={20}/>
          <span>Cyber Security</span>
        </div>

        <div className="flex items-center gap-3 hover:text-blue-400 cursor-pointer">
          <Users size={20}/>
          <span>Users</span>
        </div>

        <div className="flex items-center gap-3 hover:text-blue-400 cursor-pointer">
          <Settings size={20}/>
          <span>Settings</span>
        </div>

      </nav>

    </aside>
  );
}
