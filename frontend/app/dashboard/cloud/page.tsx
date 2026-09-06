"use client";

import { useEffect, useState } from "react";
import {
  Cloud,
  Server,
  ShieldCheck,
  Activity,
  Plus,
  RefreshCw,
  Database,
  Globe,
  AlertTriangle,
} from "lucide-react";
import API from "@/services/api";

type CloudAccount = {
  id: number;
  name: string;
  provider: string;
  account_identifier: string;
  region: string | null;
  status: string;
  is_active: boolean;
};

type CloudAsset = {
  id: number;
  cloud_account_id: number;
  provider: string;
  asset_type: string;
  asset_name: string;
  resource_id: string;
  region: string | null;
  status: string;
  risk_level: string;
  metadata_json: string | null;
  discovered_at: string;
};

export default function CloudSecurityPage() {
  const [accounts, setAccounts] = useState<CloudAccount[]>([]);
  const [assets, setAssets] = useState<CloudAsset[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAccountForm, setShowAccountForm] = useState(false);

  const [form, setForm] = useState({
    name: "",
    provider: "AWS",
    account_identifier: "",
    region: "ap-south-1",
    description: "",
  });

  const loadCloudData = async () => {
    try {
      setLoading(true);

      const [accountsResponse, assetsResponse] = await Promise.all([
        API.get("/cloud/accounts"),
        API.get("/cloud/assets"),
      ]);

      setAccounts(accountsResponse.data || []);
      setAssets(assetsResponse.data || []);
    } catch (error) {
      console.error("Cloud data loading failed:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCloudData();
  }, []);

  const createAccount = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await API.post("/cloud/accounts", form);

      setForm({
        name: "",
        provider: "AWS",
        account_identifier: "",
        region: "ap-south-1",
        description: "",
      });

      setShowAccountForm(false);
      await loadCloudData();
    } catch (error) {
      console.error("Cloud account creation failed:", error);
      alert("Unable to create cloud account.");
    }
  };

  const activeAccounts = accounts.filter((a) => a.is_active).length;

  const activeAssets = assets.filter(
    (a) => a.status?.toLowerCase() === "active"
  ).length;

  const highRiskAssets = assets.filter(
    (a) =>
      a.risk_level?.toLowerCase() === "high" ||
      a.risk_level?.toLowerCase() === "critical"
  ).length;

  return (
    <div className="min-h-screen bg-[#05070b] text-white">
      <div className="border-b border-white/10 bg-[#070a10]/90 px-5 py-5 backdrop-blur-xl lg:px-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 text-cyan-400">
              <Cloud size={25} />
            </div>

            <div>
              <h1 className="text-2xl font-bold">Cloud Security</h1>
              <p className="mt-1 text-sm text-gray-500">
                Monitor cloud accounts, assets and infrastructure security.
              </p>
            </div>
          </div>

          <div className="flex gap-2">
            <button
              onClick={loadCloudData}
              className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-gray-300 hover:bg-white/10"
            >
              <RefreshCw size={16} />
              Refresh
            </button>

            <button
              onClick={() => setShowAccountForm(!showAccountForm)}
              className="inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-black hover:bg-gray-200"
            >
              <Plus size={16} />
              Add Cloud Account
            </button>
          </div>
        </div>
      </div>

      <main className="p-5 lg:p-8">
        {showAccountForm && (
          <section className="mb-6 rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <div className="mb-5">
              <h2 className="text-lg font-semibold">Connect Cloud Account</h2>
              <p className="mt-1 text-sm text-gray-500">
                Register a cloud account in NEXUS ONE.
              </p>
            </div>

            <form
              onSubmit={createAccount}
              className="grid gap-4 md:grid-cols-2"
            >
              <input
                value={form.name}
                onChange={(e) =>
                  setForm({ ...form, name: e.target.value })
                }
                placeholder="Account Name"
                required
                className="rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm outline-none placeholder:text-gray-600 focus:border-cyan-500/50"
              />

              <select
                value={form.provider}
                onChange={(e) =>
                  setForm({ ...form, provider: e.target.value })
                }
                className="rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm outline-none"
              >
                <option value="AWS">AWS</option>
                <option value="Azure">Azure</option>
                <option value="GCP">GCP</option>
              </select>

              <input
                value={form.account_identifier}
                onChange={(e) =>
                  setForm({
                    ...form,
                    account_identifier: e.target.value,
                  })
                }
                placeholder="Account ID / Subscription ID"
                required
                className="rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm outline-none placeholder:text-gray-600 focus:border-cyan-500/50"
              />

              <input
                value={form.region}
                onChange={(e) =>
                  setForm({ ...form, region: e.target.value })
                }
                placeholder="Region"
                className="rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm outline-none placeholder:text-gray-600 focus:border-cyan-500/50"
              />

              <input
                value={form.description}
                onChange={(e) =>
                  setForm({
                    ...form,
                    description: e.target.value,
                  })
                }
                placeholder="Description"
                className="rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm outline-none placeholder:text-gray-600 focus:border-cyan-500/50 md:col-span-2"
              />

              <div className="flex gap-3 md:col-span-2">
                <button
                  type="submit"
                  className="rounded-xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-black hover:bg-cyan-400"
                >
                  Connect Account
                </button>

                <button
                  type="button"
                  onClick={() => setShowAccountForm(false)}
                  className="rounded-xl border border-white/10 px-5 py-3 text-sm text-gray-400 hover:bg-white/5"
                >
                  Cancel
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Cloud Accounts</span>
              <Cloud size={19} className="text-cyan-400" />
            </div>
            <div className="mt-4 text-3xl font-bold">
              {accounts.length}
            </div>
            <div className="mt-1 text-xs text-gray-500">
              {activeAccounts} active accounts
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Cloud Assets</span>
              <Server size={19} className="text-blue-400" />
            </div>
            <div className="mt-4 text-3xl font-bold">
              {assets.length}
            </div>
            <div className="mt-1 text-xs text-gray-500">
              {activeAssets} active assets
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Security Status</span>
              <ShieldCheck size={19} className="text-emerald-400" />
            </div>
            <div className="mt-4 text-3xl font-bold text-emerald-400">
              Protected
            </div>
            <div className="mt-1 text-xs text-gray-500">
              Cloud monitoring enabled
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">High Risk</span>
              <AlertTriangle size={19} className="text-orange-400" />
            </div>
            <div className="mt-4 text-3xl font-bold">
              {highRiskAssets}
            </div>
            <div className="mt-1 text-xs text-gray-500">
              Assets requiring attention
            </div>
          </div>
        </section>

        <section className="mb-6 rounded-2xl border border-white/10 bg-white/[0.03] p-6">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">Connected Accounts</h2>
              <p className="mt-1 text-sm text-gray-500">
                Cloud environments registered with NEXUS ONE.
              </p>
            </div>

            <Activity size={20} className="text-gray-500" />
          </div>

          {loading ? (
            <div className="py-10 text-center text-sm text-gray-500">
              Loading cloud accounts...
            </div>
          ) : accounts.length === 0 ? (
            <div className="rounded-xl border border-dashed border-white/10 py-10 text-center text-sm text-gray-500">
              No cloud accounts connected.
            </div>
          ) : (
            <div className="space-y-3">
              {accounts.map((account) => (
                <div
                  key={account.id}
                  className="flex flex-col gap-4 rounded-xl border border-white/10 bg-black/20 p-4 md:flex-row md:items-center md:justify-between"
                >
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5">
                      <Cloud size={19} />
                    </div>

                    <div>
                      <div className="font-medium">{account.name}</div>
                      <div className="mt-1 text-xs text-gray-500">
                        {account.provider} · {account.account_identifier}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs">
                    <span className="text-gray-500">
                      {account.region || "Global"}
                    </span>

                    <span
                      className={`rounded-full px-3 py-1 ${
                        account.is_active
                          ? "bg-emerald-500/10 text-emerald-400"
                          : "bg-red-500/10 text-red-400"
                      }`}
                    >
                      {account.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
          <div className="mb-5">
            <h2 className="text-lg font-semibold">Cloud Assets</h2>
            <p className="mt-1 text-sm text-gray-500">
              Discovered infrastructure across connected cloud accounts.
            </p>
          </div>

          {loading ? (
            <div className="py-10 text-center text-sm text-gray-500">
              Loading cloud assets...
            </div>
          ) : assets.length === 0 ? (
            <div className="rounded-xl border border-dashed border-white/10 py-10 text-center text-sm text-gray-500">
              No cloud assets discovered.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[760px] text-left">
                <thead>
                  <tr className="border-b border-white/10 text-xs uppercase tracking-wider text-gray-500">
                    <th className="px-4 py-3">Asset</th>
                    <th className="px-4 py-3">Provider</th>
                    <th className="px-4 py-3">Type</th>
                    <th className="px-4 py-3">Region</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3">Risk</th>
                  </tr>
                </thead>

                <tbody>
                  {assets.map((asset) => (
                    <tr
                      key={asset.id}
                      className="border-b border-white/5 text-sm hover:bg-white/[0.02]"
                    >
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-3">
                          <Server size={17} className="text-gray-500" />
                          <div>
                            <div className="font-medium">
                              {asset.asset_name}
                            </div>
                            <div className="mt-1 text-xs text-gray-600">
                              {asset.resource_id}
                            </div>
                          </div>
                        </div>
                      </td>

                      <td className="px-4 py-4">
                        {asset.provider}
                      </td>

                      <td className="px-4 py-4">
                        {asset.asset_type}
                      </td>

                      <td className="px-4 py-4 text-gray-400">
                        {asset.region || "Global"}
                      </td>

                      <td className="px-4 py-4">
                        <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
                          {asset.status}
                        </span>
                      </td>

                      <td className="px-4 py-4">
                        <span
                          className={`rounded-full px-3 py-1 text-xs ${
                            asset.risk_level === "critical"
                              ? "bg-red-500/10 text-red-400"
                              : asset.risk_level === "high"
                              ? "bg-orange-500/10 text-orange-400"
                              : "bg-emerald-500/10 text-emerald-400"
                          }`}
                        >
                          {asset.risk_level}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <footer className="mt-10 border-t border-white/10 pt-6 text-center text-xs text-gray-600">
          NEXUS ONE — Cloud Security Intelligence
        </footer>
      </main>
    </div>
  );
}
