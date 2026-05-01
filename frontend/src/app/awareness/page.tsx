import { VoterQuiz } from "@/components/VoterQuiz"
import { TurnoutChart } from "@/components/TurnoutChart"
import { ChatWidget } from "@/components/ChatWidget"
import { Sparkles, BookOpen, Fingerprint, Map, ClipboardList, IdCard, Printer, User, Mail, FileText, Vote, Landmark, Smartphone, Phone, Search } from "lucide-react"

export const metadata = {
  title: "Voter Awareness — Chunav Saathi",
  description: "Test your knowledge with our AI-powered voter awareness quiz and explore historical election data powered by BigQuery.",
}

export default function AwarenessPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 overflow-x-hidden relative">
      {/* Ambient background */}
      <div className="absolute top-0 inset-x-0 h-64 bg-gradient-to-b from-green-500/10 to-transparent -z-10 pointer-events-none" />
      <div className="absolute top-[-5%] right-[-5%] w-80 h-80 bg-green-500/8 rounded-full blur-[100px] -z-10" />

      <div className="container mx-auto px-4 py-8 space-y-8">
        {/* Page Hero */}
        <div className="max-w-2xl">
          <span className="inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-0.5 rounded-full bg-green-500/15 text-green-400 border border-green-500/20">
            <Sparkles className="w-3.5 h-3.5" /> Powered by Gemini AI
          </span>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tighter mt-3 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            Voter Awareness Hub
          </h1>
          <p className="text-slate-400 mt-2 leading-relaxed">
            Test your election knowledge with our AI-powered quiz and explore historical turnout data.
            Every Indian voter should know their rights.
          </p>
        </div>

        {/* Main Grid */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* AI Quiz */}
          <VoterQuiz />

          {/* Election Jargon Explainer */}
          <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-slate-900 to-slate-800 p-6 shadow-2xl space-y-4">
            <div>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-400" /> Election Jargon Buster
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">AI explains complex terms in plain language</p>
            </div>

            <div className="grid gap-2">
              {[
                { term: "NOTA", icon: Fingerprint },
                { term: "Delimitation", icon: Map },
                { term: "Model Code of Conduct", icon: ClipboardList },
                { term: "EPIC Card", icon: IdCard },
                { term: "VVPAT", icon: Printer },
                { term: "Returning Officer", icon: User },
                { term: "Postal Ballot", icon: Mail },
                { term: "Affidavit Disclosure", icon: FileText },
              ].map(({ term, icon: Icon }) => (
                <a
                  key={term}
                  href={`/awareness/explain?term=${encodeURIComponent(term)}`}
                  className="flex items-center gap-3 px-4 py-3 rounded-xl border border-slate-700/60 bg-slate-800/40 hover:border-orange-500/40 hover:bg-orange-500/5 transition-all group"
                >
                  <Icon className="w-5 h-5 text-slate-400 group-hover:text-orange-400 transition-colors" />
                  <span className="text-sm text-slate-300 group-hover:text-white transition-colors">{term}</span>
                  <span className="ml-auto text-slate-600 group-hover:text-orange-400 transition-colors text-xs flex items-center gap-1">Explain <span className="text-base leading-none">→</span></span>
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* Turnout Chart */}
        <TurnoutChart />

        {/* ECI Resources */}
        <div className="rounded-xl border border-white/10 bg-white/5 p-5">
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-emerald-400" /> Official Resources
          </h3>
          <div className="grid sm:grid-cols-3 gap-3">
            {[
              { label: "Voter Portal",     url: "https://voterportal.eci.gov.in",     icon: Vote },
              { label: "ECI Official",     url: "https://eci.gov.in",                 icon: Landmark },
              { label: "cVIGIL App",       url: "https://cvigil.eci.gov.in",          icon: Smartphone },
              { label: "Voter Helpline",   url: "tel:1950",                            icon: Phone },
              { label: "Affidavit Portal", url: "https://affidavit.eci.gov.in",       icon: FileText },
              { label: "Electoral Search", url: "https://electoralsearch.eci.gov.in", icon: Search },
            ].map(r => (
              <a
                key={r.label}
                href={r.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 rounded-lg border border-slate-700/40 bg-slate-800/40 hover:border-emerald-500/30 hover:bg-emerald-500/5 text-sm text-slate-300 hover:text-white transition-all group"
              >
                <r.icon className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 transition-colors" />
                <span>{r.label}</span>
              </a>
            ))}
          </div>
        </div>
      </div>

      <ChatWidget />
    </main>
  )
}
