"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Users, Calendar, Vote, Flag, Loader2 } from "lucide-react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

type Stats = {
  active_elections_count: number
  days_until_next_phase: number
  total_seats_up: number
  eligible_voters_millions: number
}

const DEFAULT_STATS: Stats = {
  active_elections_count:  2,
  days_until_next_phase:   6,
  total_seats_up:          285,
  eligible_voters_millions: 79.5,
}

const CARDS = [
  {
    key:   "active_elections_count" as keyof Stats,
    label: "Active Elections",
    unit:  " States",
    sub:   "Across India currently",
    icon:  Flag,
    color: "text-orange-400",
    subColor: "text-orange-300/70",
    glow: "shadow-orange-500/10",
  },
  {
    key:   "days_until_next_phase" as keyof Stats,
    label: "Next Phase In",
    unit:  " Days",
    sub:   "Prepare for voting day",
    icon:  Calendar,
    color: "text-green-400",
    subColor: "text-green-300/70",
    glow: "shadow-green-500/10",
  },
  {
    key:   "total_seats_up" as keyof Stats,
    label: "Total Seats Up",
    unit:  "",
    sub:   "Assembly & Parliamentary",
    icon:  Vote,
    color: "text-blue-400",
    subColor: "text-blue-300/70",
    glow: "shadow-blue-500/10",
  },
  {
    key:   "eligible_voters_millions" as keyof Stats,
    label: "Eligible Voters",
    unit:  "M",
    sub:   "Expected turnout ~65%",
    icon:  Users,
    color: "text-purple-400",
    subColor: "text-purple-300/70",
    glow: "shadow-purple-500/10",
  },
]

export function DashboardCards() {
  const [stats,   setStats]   = useState<Stats>(DEFAULT_STATS)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/v1/elections/stats`)
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(() => {
        // Keep defaults on error
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {CARDS.map(card => {
        const Icon  = card.icon
        const value = stats[card.key]

        return (
          <Card
            key={card.key}
            className={`bg-white/5 backdrop-blur-md border border-white/10 text-white shadow-xl ${card.glow} hover:border-white/20 hover:-translate-y-0.5 transition-all duration-200`}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-300">{card.label}</CardTitle>
              <div className={`p-1.5 rounded-lg bg-white/5`}>
                <Icon className={`h-4 w-4 ${card.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Loader2 className="h-6 w-6 animate-spin text-slate-400" />
              ) : (
                <>
                  <div className="text-3xl font-bold tracking-tight">
                    {typeof value === "number" && !Number.isInteger(value)
                      ? value.toFixed(1)
                      : value}
                    <span className="text-lg font-normal text-slate-300">{card.unit}</span>
                  </div>
                  <p className={`text-xs mt-1 ${card.subColor}`}>{card.sub}</p>
                </>
              )}
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
