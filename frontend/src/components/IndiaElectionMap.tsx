"use client"

import { useState } from "react"
import { ComposableMap, Geographies, Geography, ZoomableGroup } from "react-simple-maps"
import { MapPin } from "lucide-react"

type StateStatus = "active" | "upcoming" | "none"

type StateData = {
  name: string
  status: StateStatus
  seats?: number
  nextDate?: string
}

// Simplified India state data (Keys must match topojson properties.name exactly, or standard spellings)
const STATE_DATA: Record<string, StateData> = {
  "West Bengal":     { name: "West Bengal",     status: "upcoming", seats: 42,  nextDate: "May 7, 2026" },
  "Bihar":           { name: "Bihar",           status: "upcoming", seats: 243, nextDate: "Jun 15, 2026" },
  "Uttar Pradesh":   { name: "Uttar Pradesh",   status: "upcoming", seats: 10,  nextDate: "Jul 10, 2026" },
  "Maharashtra":     { name: "Maharashtra",     status: "none" },
  "Rajasthan":       { name: "Rajasthan",       status: "none" },
  "Madhya Pradesh":  { name: "Madhya Pradesh",  status: "none" },
  "Gujarat":         { name: "Gujarat",         status: "none" },
  "Karnataka":       { name: "Karnataka",       status: "none" },
  "Tamil Nadu":      { name: "Tamil Nadu",      status: "none" },
  "Andhra Pradesh":  { name: "Andhra Pradesh",  status: "none" },
  "Telangana":       { name: "Telangana",       status: "none" },
  "Kerala":          { name: "Kerala",          status: "none" },
  "Punjab":          { name: "Punjab",          status: "none" },
  "Haryana":         { name: "Haryana",         status: "none" },
  "Jharkhand":       { name: "Jharkhand",       status: "none" },
  "Odisha":          { name: "Odisha",          status: "none" },
  "Assam":           { name: "Assam",           status: "none" },
  "Delhi":           { name: "NCT of Delhi",    status: "none" },
}

const STATUS_COLORS: Record<StateStatus, { fill: string; stroke: string; label: string }> = {
  active:   { fill: "rgba(34, 197, 94, 0.9)",  stroke: "#16a34a", label: "Voting Active" },
  upcoming: { fill: "rgba(249, 115, 22, 0.9)", stroke: "#ea580c", label: "Election Scheduled" },
  none:     { fill: "rgba(30, 41, 59, 0.8)",   stroke: "rgba(51, 65, 85, 0.5)", label: "No Upcoming Election" },
}

const geoUrl = "/india-states.json"

export function IndiaElectionMap() {
  const [hovered, setHovered] = useState<string | null>(null)
  const [tooltip, setTooltip] = useState({ x: 0, y: 0, visible: false })

  const hoveredState = hovered ? STATE_DATA[hovered] : null
  const colors       = hoveredState ? STATUS_COLORS[hoveredState.status] : null

  return (
    <div className="rounded-2xl border border-white/10 bg-slate-900/50 backdrop-blur-xl p-6 shadow-2xl relative h-full flex flex-col" role="figure" aria-label="Interactive map showing election status across Indian states">
      <div className="mb-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <MapPin className="w-5 h-5 text-rose-400" /> India Election Map
        </h3>
        <p className="text-sm text-slate-400 mt-1">Interactive geographic visualization of upcoming elections</p>
      </div>

      {/* Legend */}
      <div className="flex gap-4 mb-6 flex-wrap bg-slate-950/40 p-3 rounded-xl border border-white/5">
        {Object.entries(STATUS_COLORS).map(([status, cfg]) => (
          <div key={status} className="flex items-center gap-2">
            <div className="w-3.5 h-3.5 rounded-full shadow-inner" style={{ backgroundColor: cfg.fill, border: `1px solid ${cfg.stroke}` }} />
            <span className="text-sm text-slate-300 font-medium">{cfg.label}</span>
          </div>
        ))}
      </div>

      {/* SVG Map Container */}
      <div className="relative w-full flex-1 min-h-[400px] flex items-center justify-center bg-slate-950/20 rounded-xl border border-white/5 overflow-hidden" aria-hidden="true">
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{ scale: 800, center: [80, 22] }} // Center of India
          className="w-full h-full"
          style={{ filter: "drop-shadow(0 10px 15px rgba(0,0,0,0.5))" }}
        >
          <ZoomableGroup zoom={1} maxZoom={4}>
            <Geographies geography={geoUrl}>
              {({ geographies }) =>
                geographies.map((geo) => {
                  const stateName = geo.properties.name
                  const data   = STATE_DATA[stateName]
                  const status: StateStatus = data?.status || "none"
                  const cfg    = STATUS_COLORS[status]
                  const isHov  = hovered === stateName

                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      onMouseEnter={(e) => {
                        if (data) setHovered(stateName)
                        setTooltip({ x: e.clientX, y: e.clientY, visible: !!data })
                      }}
                      onMouseMove={(e) => {
                        if (data) setTooltip(t => ({ ...t, x: e.clientX, y: e.clientY }))
                      }}
                      onMouseLeave={() => {
                        setHovered(null)
                        setTooltip(t => ({ ...t, visible: false }))
                      }}
                      style={{
                        default: {
                          fill: cfg.fill,
                          stroke: cfg.stroke,
                          strokeWidth: 0.5,
                          outline: "none",
                          transition: "all 250ms ease"
                        },
                        hover: {
                          fill: cfg.stroke, // slightly darker on hover
                          stroke: "#fff",
                          strokeWidth: 1,
                          outline: "none",
                          cursor: data ? "pointer" : "default",
                          transition: "all 250ms ease"
                        },
                        pressed: {
                          fill: cfg.stroke,
                          stroke: "#fff",
                          strokeWidth: 1.5,
                          outline: "none",
                        },
                      }}
                    />
                  )
                })
              }
            </Geographies>
          </ZoomableGroup>
        </ComposableMap>

        {/* Tooltip */}
        {tooltip.visible && hoveredState && (
          <div
            className="fixed pointer-events-none z-50 bg-slate-900/95 backdrop-blur-md border border-white/20 rounded-xl px-4 py-3 text-sm text-white shadow-2xl animate-in fade-in zoom-in-95 duration-200"
            style={{
              left: tooltip.x + 15,
              top:  tooltip.y + 15,
              minWidth: "180px",
            }}
          >
            <p className="font-bold text-base text-white">{hoveredState.name}</p>
            <div className="flex items-center gap-1.5 mt-1">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: colors?.fill }} />
              <p className="text-slate-300 font-medium text-xs uppercase tracking-wider">{colors?.label}</p>
            </div>
            
            {(hoveredState.seats || hoveredState.nextDate) && (
              <div className="mt-3 pt-3 border-t border-white/10 space-y-1.5">
                {hoveredState.seats && (
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-xs">Total Seats</span>
                    <span className="font-semibold">{hoveredState.seats}</span>
                  </div>
                )}
                {hoveredState.nextDate && (
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-xs">Poll Date</span>
                    <span className="text-orange-400 font-semibold">{hoveredState.nextDate}</span>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
