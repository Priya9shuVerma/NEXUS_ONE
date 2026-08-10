import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="text-center">

        <h1 className="text-6xl font-bold tracking-wide">
          NEXUS ONE
        </h1>

        <p className="mt-5 text-xl text-gray-400">
          AI Powered Enterprise Intelligence Platform
        </p>

        <div className="mt-8 flex gap-4 justify-center">

          <Link
            href="/ai"
            className="
              px-8
              py-3
              rounded-xl
              bg-blue-600
              hover:bg-blue-700
              transition
              font-semibold
            "
          >
            Start AI Assistant
          </Link>

          <Link
            href="/ai"
            className="
              px-8
              py-3
              rounded-xl
              border
              border-gray-600
              hover:bg-gray-800
              transition
              font-semibold
            "
          >
            Open AI
          </Link>

        </div>

      </div>
    </main>
  );
}
