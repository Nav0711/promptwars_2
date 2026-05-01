export default function ElectionsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <h1 className="text-3xl font-bold mb-6">Live Election Tracker</h1>
      <p className="text-slate-400 mb-8">Track real-time status of ongoing and upcoming elections across India.</p>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="p-6 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm">
          <h2 className="text-xl font-semibold mb-2">State Elections</h2>
          <p className="text-sm text-slate-400">Loading active state elections...</p>
        </div>
        <div className="p-6 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm">
          <h2 className="text-xl font-semibold mb-2">By-Elections</h2>
          <p className="text-sm text-slate-400">Loading active by-elections...</p>
        </div>
      </div>
    </main>
  )
}
