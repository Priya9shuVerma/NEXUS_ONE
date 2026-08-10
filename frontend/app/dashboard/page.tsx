"use client";

import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import DashboardCard from "@/components/DashboardCard";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function DashboardPage() {

  return (

    <ProtectedRoute>

      <div className="flex min-h-screen bg-black">

        <Sidebar />

        <div className="flex-1">

          <Navbar />

          <div className="p-8 space-y-8">

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

              <DashboardCard
                title="Users"
                value="125"
              />

              <DashboardCard
                title="AI Requests"
                value="985"
              />

              <DashboardCard
                title="Threat Alerts"
                value="12"
              />

            </div>

            <div className="grid md:grid-cols-2 gap-6">

              <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">

                <h2 className="text-2xl font-bold text-white mb-6">
                  AI System Status
                </h2>

                <div className="space-y-4">

                  <div className="flex justify-between">
                    <span className="text-gray-400">AI Engine</span>
                    <span className="text-green-400">Online</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-400">Knowledge Base</span>
                    <span className="text-green-400">Ready</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-400">Embedding Model</span>
                    <span className="text-green-400">Loaded</span>
                  </div>

                </div>

              </div>

              <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">

                <h2 className="text-2xl font-bold text-white mb-6">
                  Security Monitor
                </h2>

                <div className="space-y-4">

                  <div className="flex justify-between">
                    <span className="text-gray-400">Firewall</span>
                    <span className="text-green-400">Active</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-400">Threat Scan</span>
                    <span className="text-yellow-400">Running</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-400">Risk Level</span>
                    <span className="text-red-400">Medium</span>
                  </div>

                </div>

              </div>

            </div>

            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">

              <h2 className="text-2xl font-bold text-white mb-6">
                Recent Activity
              </h2>

              <div className="space-y-3">

                <div className="flex justify-between text-gray-300">
                  <span>User Login</span>
                  <span>2 min ago</span>
                </div>

                <div className="flex justify-between text-gray-300">
                  <span>AI Question Asked</span>
                  <span>5 min ago</span>
                </div>

                <div className="flex justify-between text-gray-300">
                  <span>Threat Scan Completed</span>
                  <span>12 min ago</span>
                </div>

                <div className="flex justify-between text-gray-300">
                  <span>Knowledge Base Updated</span>
                  <span>35 min ago</span>
                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </ProtectedRoute>

  );

}
