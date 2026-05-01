"use client"
import { useState } from "react"
import { ChevronDown, Search } from "lucide-react"
import { Input } from "@/components/ui/input"

const faqs = [
  {
    q: "How do I check if my name is on the voter list?",
    a: "You can verify your name on the electoral roll by visiting the official Voter Portal at voterportal.eci.gov.in and entering your EPIC number or basic details."
  },
  {
    q: "What documents are valid for voting?",
    a: "The standard document is your Voter ID (EPIC card). However, the ECI also permits alternate photo ID documents like Aadhaar, PAN card, Driving License, or Passport if specified in the official notification."
  },
  {
    q: "How does the EVM work?",
    a: "An Electronic Voting Machine (EVM) consists of a Control Unit and a Balloting Unit. When you press the button next to your candidate, a beep confirms your vote. It is paired with a VVPAT machine that prints a slip of your vote for verification."
  },
  {
    q: "What is the Model Code of Conduct (MCC)?",
    a: "The MCC is a set of guidelines issued by the ECI to regulate political parties and candidates prior to elections, ensuring free and fair polling. It comes into force as soon as the election schedule is announced."
  }
]

export default function FAQsPage() {
  const [open, setOpen] = useState<number | null>(0)
  const [query, setQuery] = useState("")

  const filteredFaqs = faqs.filter(f => f.q.toLowerCase().includes(query.toLowerCase()) || f.a.toLowerCase().includes(query.toLowerCase()))

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Election FAQs & Knowledge Base</h1>
        <p className="text-slate-400 mb-8">Find answers to common questions regarding the voting process, registration, and more.</p>
        
        <div className="relative mb-8">
          <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
          <Input 
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search questions..." 
            className="pl-10 bg-white/5 border-white/10 text-white placeholder:text-slate-500"
          />
        </div>

        <div className="space-y-4">
          {filteredFaqs.length === 0 && <p className="text-slate-500">No questions found matching your search.</p>}
          {filteredFaqs.map((faq, i) => (
            <div key={i} className="rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm overflow-hidden transition-all">
              <button 
                onClick={() => setOpen(open === i ? null : i)}
                className="w-full flex items-center justify-between p-6 text-left hover:bg-white/5 transition-colors"
              >
                <h3 className="text-lg font-medium pr-4">{faq.q}</h3>
                <ChevronDown className={`h-5 w-5 text-slate-400 transition-transform ${open === i ? 'rotate-180' : ''}`} />
              </button>
              {open === i && (
                <div className="px-6 pb-6 text-slate-300 animate-in fade-in slide-in-from-top-2">
                  <div className="w-full h-px bg-white/10 mb-4" />
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}
