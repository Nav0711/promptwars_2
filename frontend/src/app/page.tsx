import { DashboardCards } from "@/components/DashboardCards"
import { ChatWidget } from "@/components/ChatWidget"
import { PhaseTimeline } from "@/components/PhaseTimeline"
import dynamic from "next/dynamic"
import { Skeleton } from "@/components/ui/skeleton"

const IndiaElectionMap = dynamic(
  () => import("@/components/IndiaElectionMap").then((mod) => mod.IndiaElectionMap),
  { 
    ssr: false,
    loading: () => <Skeleton className="w-full min-h-[400px] rounded-2xl bg-slate-900/50" />
  }
)
import Link from "next/link"
import { Activity, BrainCircuit, CalendarDays, MapPin, Cpu, ArrowUpRight } from "lucide-react"

export const metadata = {
  title: "Chunav Saathi — India Election Intelligence",
  description: "Real-time election schedules, unbiased candidate data, and your intelligent civic assistant powered by AI.",
}

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 overflow-x-hidden relative">
      {/* Ambient background decorations */}
      <div className="absolute top-0 inset-x-0 h-96 bg-gradient-to-b from-orange-500/10 via-slate-950/50 to-transparent -z-10 pointer-events-none" />
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-green-500/10 rounded-full blur-[120px] -z-10" />
      <div className="absolute top-[20%] right-[-5%] w-96 h-96 bg-orange-500/10 rounded-full blur-[120px] -z-10" />

      <div className="container mx-auto px-4 py-12 md:py-16 space-y-12">
        {/* Hero Section */}
        <div className="flex flex-col space-y-6 max-w-4xl mx-auto text-center items-center animate-in fade-in slide-in-from-bottom-8 duration-700 ease-out">
          <div className="flex items-center gap-2 mb-2">
            <span className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20 backdrop-blur-sm">
              <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
              Live &middot; Powered by Vertex AI
            </span>
          </div>
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-slate-200 to-slate-500 pb-2">
            India Election Intelligence Hub
          </h1>
          <p className="text-lg md:text-xl text-slate-400 leading-relaxed max-w-2xl">
            Your single source of truth for the world&apos;s largest democracy. Real-time schedules,
            unbiased candidate data, and your intelligent civic assistant.
          </p>
          <div className="flex flex-wrap justify-center gap-4 pt-4">
            <Link
              href="/tracker"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-orange-500 hover:bg-orange-600 text-white text-sm font-semibold transition-all hover:-translate-y-1 shadow-lg shadow-orange-500/25"
            >
              <Activity className="w-4 h-4" />
              Live Tracker
            </Link>
            <Link
              href="/awareness"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 text-slate-200 hover:text-white text-sm font-medium transition-all backdrop-blur-sm"
            >
              <BrainCircuit className="w-4 h-4 text-green-400" />
              Voter Quiz
            </Link>
            <Link
              href="/elections"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 text-slate-200 hover:text-white text-sm font-medium transition-all backdrop-blur-sm"
            >
              <CalendarDays className="w-4 h-4 text-blue-400" />
              Schedule
            </Link>
            <Link
              href="/booth"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 text-slate-200 hover:text-white text-sm font-medium transition-all backdrop-blur-sm"
            >
              <MapPin className="w-4 h-4 text-rose-400" />
              Find Booth
            </Link>
          </div>
        </div>

        {/* Dashboard Cards */}
        <div className="animate-in fade-in slide-in-from-bottom-12 duration-1000 delay-150 ease-out fill-mode-both">
          <DashboardCards />
        </div>

        {/* Timeline + Map Grid */}
        <div className="grid lg:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-16 duration-1000 delay-300 ease-out fill-mode-both">
          <div className="lg:col-span-5 flex flex-col">
            <PhaseTimeline />
          </div>
          <div className="lg:col-span-7 flex flex-col">
            <IndiaElectionMap />
          </div>
        </div>

        {/* Footer Banner */}
        <div className="rounded-2xl border border-white/10 bg-slate-900/50 backdrop-blur-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-6 animate-in fade-in duration-1000 delay-500 fill-mode-both">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-full bg-blue-500/10 flex items-center justify-center border border-blue-500/20 shrink-0">
              <Cpu className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <p className="text-sm font-semibold text-white">Powered by Vertex AI & Firestore</p>
              <p className="text-sm text-slate-400 mt-0.5">
                Information sourced from official ECI documents.
              </p>
            </div>
          </div>
          <a
            href="https://eci.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-orange-400 hover:text-orange-300 transition-colors shrink-0"
          >
            Visit ECI Portal <ArrowUpRight className="w-4 h-4" />
          </a>
        </div>
      </div>

      {/* Floating Chat Widget */}
      <ChatWidget />
    </main>
  )
}
