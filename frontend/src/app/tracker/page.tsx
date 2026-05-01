import { ElectionTracker } from "@/components/ElectionTracker"
import { ChatWidget } from "@/components/ChatWidget"
import Link from "next/link"
import { MapPin, BrainCircuit, ExternalLink, Bell } from "lucide-react"

export const metadata = {
  title: "Live Election Tracker — Chunav Saathi",
  description: "Track all upcoming and active Indian elections in real-time. Phase-wise schedules, countdown timers, and live status updates.",
}

export default function TrackerPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 overflow-x-hidden relative">
      {/* Ambient background */}
      <div className="absolute top-0 inset-x-0 h-64 bg-gradient-to-b from-orange-500/15 to-transparent -z-10 pointer-events-none" />
      <div className="absolute top-[-5%] left-[-5%] w-80 h-80 bg-orange-500/8 rounded-full blur-[100px] -z-10" />

      <div className="container mx-auto px-4 py-8 space-y-8">
        {/* Page Hero */}
        <div className="max-w-2xl">
          <div className="flex items-center gap-2 mb-3">
            <span className="flex items-center gap-1.5 text-xs font-medium px-2.5 py-0.5 rounded-full bg-red-500/15 text-red-400 border border-red-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse" />
              LIVE
            </span>
            <span className="text-xs text-slate-500">Auto-updates every visit</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            Live Election Tracker
          </h1>
          <p className="text-slate-400 mt-2 leading-relaxed">
            Real-time phase-wise tracker for all Indian elections. Phase status is computed dynamically
            based on today&apos;s date against official ECI schedules.
          </p>
        </div>

        {/* Key Actions */}
        <div className="flex flex-wrap gap-3">
          <Link
            href="/booth"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/20 hover:border-green-500/50 text-slate-300 hover:text-white text-sm font-medium transition-all"
          >
            <MapPin className="w-4 h-4 text-rose-400" /> Find My Polling Booth
          </Link>
          <Link
            href="/awareness"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/20 hover:border-orange-500/50 text-slate-300 hover:text-white text-sm font-medium transition-all"
          >
            <BrainCircuit className="w-4 h-4 text-green-400" /> Voter Awareness Quiz
          </Link>
          <a
            href="https://eci.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/20 hover:border-blue-500/50 text-slate-300 hover:text-white text-sm font-medium transition-all"
          >
            <ExternalLink className="w-4 h-4 text-blue-400" /> ECI Official
          </a>
        </div>

        {/* Tracker */}
        <ElectionTracker />

        {/* Notification Prompt */}
        <div className="rounded-xl border border-white/10 bg-white/5 p-5 flex flex-col sm:flex-row items-center gap-4">
          <div className="flex-1">
            <p className="text-sm font-semibold text-white flex items-center gap-2"><Bell className="w-4 h-4 text-amber-400" /> Stay Updated</p>
            <p className="text-xs text-slate-400 mt-0.5">
              Set a reminder for your state&apos;s election. Ask Chunav Saathi in the chat below!
            </p>
          </div>
          <button
            className="text-sm px-4 py-2 rounded-full bg-orange-500 hover:bg-orange-600 text-white font-medium transition-all shrink-0"
          >
            Ask Chunav Saathi →
          </button>
        </div>
      </div>

      <ChatWidget />
    </main>
  )
}
