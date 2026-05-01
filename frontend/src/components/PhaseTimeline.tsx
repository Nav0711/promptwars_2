import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function PhaseTimeline() {
  const phases = [
    { phase: 1, date: "May 7, 2026", status: "Completed", seats: 102 },
    { phase: 2, date: "May 14, 2026", status: "Active", seats: 89 },
    { phase: 3, date: "May 21, 2026", status: "Upcoming", seats: 94 },
    { phase: 4, date: "May 28, 2026", status: "Upcoming", seats: 96 },
  ]

  return (
    <Card className="bg-white/10 backdrop-blur-md border-white/20 text-white shadow-xl shadow-black/10">
      <CardHeader>
        <CardTitle className="text-xl">Election Phase Timeline</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative border-l border-white/20 ml-3 space-y-6">
          {phases.map((p, idx) => (
            <div key={idx} className="relative pl-6">
              <div className={`absolute -left-1.5 top-1.5 h-3 w-3 rounded-full border-2 border-slate-950 ${p.status === 'Completed' ? 'bg-green-500' : p.status === 'Active' ? 'bg-orange-500 animate-pulse' : 'bg-slate-400'}`} />
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-semibold">Phase {p.phase}</h4>
                  <p className="text-sm text-slate-300">{p.date}</p>
                </div>
                <div className="text-right">
                  <span className={`text-xs px-2 py-1 rounded-full ${p.status === 'Completed' ? 'bg-green-500/20 text-green-300' : p.status === 'Active' ? 'bg-orange-500/20 text-orange-300' : 'bg-slate-500/20 text-slate-300'}`}>
                    {p.status}
                  </span>
                  <p className="text-xs text-slate-400 mt-1">{p.seats} Seats</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
