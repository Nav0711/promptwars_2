"use client"
import { useState } from "react"
import { Search, MapPin } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function BoothFinderPage() {
  const [query, setQuery] = useState("")
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (!query) return
    setLoading(true)
    setTimeout(() => {
      setResult({
        name: "Govt. Senior Secondary School",
        room: "Room No. 4",
        address: "Sector 12, Main Road, New Delhi 110001",
        officer: "Rajesh Kumar (BLO)",
        accessible: true
      })
      setLoading(false)
    }, 1000)
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <h1 className="text-3xl font-bold mb-6">Polling Booth Finder</h1>
      <p className="text-slate-400 mb-8 max-w-2xl">Locate your designated polling station based on your EPIC number (Voter ID). We use official ECI records to find the most accurate location for you.</p>
      
      <div className="max-w-xl p-6 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm">
        <form onSubmit={handleSearch} className="flex gap-2">
          <Input 
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Enter EPIC Number (e.g., ABC1234567)" 
            className="bg-white/10 border-white/20 text-white placeholder:text-slate-400 flex-1"
          />
          <Button type="submit" disabled={loading} className="bg-orange-500 hover:bg-orange-600 text-white">
            <Search className="h-4 w-4 md:mr-2" />
            <span className="hidden md:inline">{loading ? "Searching..." : "Search"}</span>
          </Button>
        </form>

        {result && (
          <div className="mt-8 pt-8 border-t border-white/10 animate-in fade-in slide-in-from-bottom-4">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-full bg-green-500/20 text-green-400 flex items-center justify-center shrink-0">
                <MapPin className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">{result.name}</h3>
                <p className="text-slate-300 mt-1">{result.room}</p>
                <p className="text-slate-400 text-sm mt-2">{result.address}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  <span className="px-2 py-1 text-xs rounded bg-slate-800 text-slate-300 border border-slate-700">BLO: {result.officer}</span>
                  {result.accessible && <span className="px-2 py-1 text-xs rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">♿ Wheelchair Accessible</span>}
                </div>
              </div>
            </div>
            <div className="mt-6 h-48 bg-slate-900 rounded-lg border border-slate-800 flex items-center justify-center text-slate-500 text-sm overflow-hidden relative">
              <div className="absolute inset-0 opacity-50 bg-[url('https://maps.googleapis.com/maps/api/staticmap?center=28.6139,77.2090&zoom=14&size=600x300&maptype=roadmap&markers=color:red%7Clabel:P%7C28.6139,77.2090&key=MOCK_KEY')] bg-cover bg-center" />
              <span className="relative z-10 bg-slate-950/80 px-4 py-2 rounded-md">Interactive Map Placeholder</span>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
