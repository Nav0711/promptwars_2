"use client"

import { useEffect, useState } from "react"
import { Calendar, CheckCircle2, Clock, Loader2, AlertCircle } from "lucide-react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

type Phase = {
  id: string
  state: string
  type: string
  phase: number
  date: string
  constituencies: number
  total_seats: number
  status: "UPCOMING" | "VOTING_TODAY" | "COMPLETED"
  days_away: number
}

type TrackerData = {
  phases: Phase[]
  last_updated: string
  next_phase: Phase | null
}

const STATUS_CONFIG = {
  VOTING_TODAY: {
    label:  "Voting Today!",
    badge:  "bg-green-500 text-white animate-pulse",
    card:   "border-green-500/40 bg-green-500/5",
    icon:   CheckCircle2,
    color:  "text-green-400",
  },
  UPCOMING: {
    label:  "Upcoming",
    badge:  "bg-orange-500/20 text-orange-300 border border-orange-500/30",
    card:   "border-orange-500/20 bg-orange-500/5",
    icon:   Clock,
    color:  "text-orange-400",
  },
  COMPLETED: {
    label:  "Completed",
    badge:  "bg-slate-600/40 text-slate-400 border border-slate-600/30",
    card:   "border-slate-700/40 bg-slate-800/40",
    icon:   CheckCircle2,
    color:  "text-slate-500",
  },
}

function Countdown({ days }: { days: number }) {
  if (days === 0) return <span className="text-green-400 font-bold text-lg animate-pulse">TODAY</span>
  if (days > 365) return null
  return (
    <div className="flex items-center gap-1.5">
      <span className="text-2xl font-bold text-white">{days}</span>
      <span className="text-sm text-slate-400">days away</span>
    </div>
  )
}

export function ElectionTracker() {
  const [data,    setData]    = useState<TrackerData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(false)

  useEffect(() => {
    fetch(`${API_BASE}/v1/elections/tracker`)
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => { setError(true); setLoading(false) })
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center py-20">
      <Loader2 className="h-8 w-8 text-orange-400 animate-spin" />
    </div>
  )

  if (error || !data) return (
    <div className="flex flex-col items-center justify-center py-16 gap-3 text-slate-400">
      <AlertCircle className="h-8 w-8" />
      <p>Could not load tracker data. Please try again.</p>
    </div>
  )

  const upcomingCount  = data.phases.filter(p => p.status === "UPCOMING").length
  const completedCount = data.phases.filter(p => p.status === "COMPLETED").length
  const todayCount     = data.phases.filter(p => p.status === "VOTING_TODAY").length

  return (
    <div className="space-y-6">
      {/* Next Phase Banner */}
      {data.next_phase && (
        <div className="rounded-2xl border border-orange-500/30 bg-gradient-to-r from-orange-500/10 to-amber-500/5 p-5">
          <p className="text-xs text-orange-400 font-semibold uppercase tracking-widest mb-1">Next Election Phase</p>
          <h2 className="text-xl font-bold text-white">
            {data.next_phase.state} — Phase {data.next_phase.phase}
          </h2>
          <p className="text-slate-400 text-sm mt-0.5">{data.next_phase.type}</p>
          <div className="flex items-center gap-4 mt-3">
            <Countdown days={data.next_phase.days_away} />
            <div className="h-8 w-px bg-slate-700" />
            <div>
              <p className="text-xs text-slate-500">Polling Date</p>
              <p className="text-sm font-semibold text-white">
                {new Date(data.next_phase.date).toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" })}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Constituencies</p>
              <p className="text-sm font-semibold text-white">{data.next_phase.constituencies}</p>
            </div>
          </div>
        </div>
      )}

      {/* Summary pills */}
      <div className="flex flex-wrap gap-2">
        {todayCount > 0 && (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-green-500/20 text-green-300 border border-green-500/30 text-xs font-medium animate-pulse">
            <CheckCircle2 className="w-3.5 h-3.5" /> {todayCount} Voting Today
          </span>
        )}
        <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-500/20 text-orange-300 border border-orange-500/30 text-xs font-medium">
          <Clock className="w-3.5 h-3.5" /> {upcomingCount} Upcoming
        </span>
        <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-700/40 text-slate-400 border border-slate-700/30 text-xs font-medium">
          <CheckCircle2 className="w-3.5 h-3.5" /> {completedCount} Completed
        </span>
      </div>

      {/* Phase Cards */}
      <div className="space-y-3">
        {data.phases.map((phase) => {
          const cfg  = STATUS_CONFIG[phase.status]
          const Icon = cfg.icon
          return (
            <div
              key={phase.id}
              className={`rounded-xl border p-4 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg ${cfg.card}`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${cfg.badge}`}>
                      {cfg.label}
                    </span>
                    <span className="text-xs text-slate-500">Phase {phase.phase}</span>
                  </div>
                  <h3 className={`font-semibold ${phase.status === "COMPLETED" ? "text-slate-400" : "text-white"}`}>
                    {phase.state}
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">{phase.type}</p>

                  <div className="flex items-center gap-4 mt-2">
                    <div className="flex items-center gap-1.5 text-xs text-slate-400">
                      <Calendar className="h-3.5 w-3.5" />
                      {new Date(phase.date).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}
                    </div>
                    <span className="text-xs text-slate-500">{phase.constituencies} constituencies</span>
                    <span className="text-xs text-slate-500">{phase.total_seats} seats</span>
                  </div>
                </div>

                <div className="text-right shrink-0">
                  {phase.status === "UPCOMING" && (
                    <>
                      <p className="text-2xl font-bold text-white">{phase.days_away}</p>
                      <p className="text-xs text-slate-500">days</p>
                    </>
                  )}
                  {phase.status === "VOTING_TODAY" && (
                    <Icon className="h-8 w-8 text-green-400 animate-pulse" />
                  )}
                  {phase.status === "COMPLETED" && (
                    <Icon className="h-6 w-6 text-slate-500" />
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <p className="text-xs text-slate-600 text-right">
        Last updated: {new Date(data.last_updated).toLocaleTimeString("en-IN")}
      </p>
    </div>
  )
}
