"use client"

import { useEffect, useState } from "react"
import { Loader2, BarChart3 } from "lucide-react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

type TurnoutRow = {
  state: string
  year: number
  turnout_pct: number
  registered_voters: number
}

// Simple bar chart using pure CSS/HTML — no chart library needed
function TurnoutBar({ label, pct, year, color }: { label: string; pct: number; year: number; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs text-slate-400">
        <span>{label} ({year})</span>
        <span className="font-semibold text-white">{pct.toFixed(1)}%</span>
      </div>
      <div className="h-6 rounded-lg bg-slate-800/60 overflow-hidden">
        <div
          className={`h-full rounded-lg flex items-center px-2 text-xs text-white font-medium transition-all duration-700 ${color}`}
          style={{ width: `${pct}%` }}
        >
          {pct > 20 ? `${pct.toFixed(1)}%` : ""}
        </div>
      </div>
    </div>
  )
}

const STATE_COLORS = [
  "bg-orange-500",
  "bg-amber-500",
  "bg-green-500",
  "bg-blue-500",
  "bg-purple-500",
  "bg-rose-500",
]

export function TurnoutChart() {
  const [data,    setData]    = useState<TurnoutRow[]>([])
  const [loading, setLoading] = useState(true)
  const [summary, setSummary] = useState<{ avg_turnout?: number; total_registered?: number } | null>(null)

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/v1/elections/analytics/turnout`).then(r => r.json()),
      fetch(`${API_BASE}/v1/elections/analytics/summary`).then(r => r.json()),
    ])
      .then(([turnout, sum]) => {
        setData(turnout.data || [])
        setSummary(sum)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  // Group by state for color assignment
  const states = [...new Set(data.map(d => d.state))]

  return (
    <div className="rounded-2xl border border-white/10 bg-slate-900/80 p-6 shadow-2xl space-y-6">
      <div>
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-indigo-400" /> Historical Voter Turnout
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">Powered by BigQuery — chunav_analytics dataset</p>
      </div>

      {/* National summary pills */}
      {summary && (
        <div className="flex flex-wrap gap-3">
          <div className="px-4 py-2 rounded-xl bg-orange-500/10 border border-orange-500/20">
            <p className="text-xs text-slate-400">National Avg. Turnout</p>
            <p className="text-xl font-bold text-orange-300">{summary.avg_turnout?.toFixed(1)}%</p>
          </div>
          <div className="px-4 py-2 rounded-xl bg-blue-500/10 border border-blue-500/20">
            <p className="text-xs text-slate-400">Total Registered Voters</p>
            <p className="text-xl font-bold text-blue-300">
              {summary.total_registered ? (summary.total_registered / 1_000_000).toFixed(0) + "M" : "—"}
            </p>
          </div>
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-8">
          <Loader2 className="h-6 w-6 text-orange-400 animate-spin" />
        </div>
      ) : (
        <div className="space-y-6">
          {states.map((state, si) => {
            const rows = data
              .filter(d => d.state === state)
              .sort((a, b) => b.year - a.year)
            const color = STATE_COLORS[si % STATE_COLORS.length]

            return (
              <div key={state}>
                <p className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${color}`} />
                  {state}
                </p>
                <div className="space-y-2 pl-4">
                  {rows.map(row => (
                    <TurnoutBar
                      key={`${state}-${row.year}`}
                      label={state}
                      pct={row.turnout_pct}
                      year={row.year}
                      color={color}
                    />
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
