"use client";

import { Users, BrainCircuit, ShieldAlert } from "lucide-react";

type Props = {
  title: string;
  value: string;
};

export default function DashboardCard({
  title,
  value,
}: Props) {

  const getIcon = () => {

    switch (title) {

      case "Users":
        return <Users size={40} className="text-blue-400" />;

      case "AI Requests":
        return <BrainCircuit size={40} className="text-green-400" />;

      case "Threat Alerts":
        return <ShieldAlert size={40} className="text-red-400" />;

      default:
        return null;
    }

  };

  return (

    <div className="bg-zinc-900 rounded-2xl border border-zinc-800 p-6 shadow-lg hover:border-blue-500 transition">

      <div className="flex justify-between items-center">

        <div>

          <h3 className="text-gray-400">
            {title}
          </h3>

          <p className="text-4xl font-bold text-white mt-4">
            {value}
          </p>

        </div>

        {getIcon()}

      </div>

    </div>

  );

}
