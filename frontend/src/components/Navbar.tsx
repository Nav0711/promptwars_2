"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Menu, X, Globe } from "lucide-react"

const NAV_LINKS = {
  en: [
    { label: "Dashboard",    href: "/" },
    { label: "Live Tracker", href: "/tracker" },
    { label: "Awareness",    href: "/awareness" },
    { label: "Find Booth",   href: "/booth" },
    { label: "FAQs",         href: "/faqs" },
  ],
  hi: [
    { label: "डैशबोर्ड",     href: "/" },
    { label: "लाइव ट्रैकर",  href: "/tracker" },
    { label: "जागरूकता",     href: "/awareness" },
    { label: "बूथ खोजें",   href: "/booth" },
    { label: "FAQ",          href: "/faqs" },
  ],
}

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [lang, setLang]     = useState<"en" | "hi">("en")
  const pathname            = usePathname()

  const links = NAV_LINKS[lang]

  return (
    <header className="border-b border-white/10 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-orange-400 to-green-500 flex items-center justify-center font-bold text-white shadow-lg group-hover:scale-105 transition-transform">
            CS
          </div>
          <span className="text-xl font-semibold tracking-tight text-white">
            Chunav Saathi
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1 text-sm font-medium">
          {links.map(link => (
            <Link
              key={link.href}
              href={link.href}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                pathname === link.href
                  ? "text-white bg-orange-500/20 border border-orange-500/30"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          {/* Language Toggle */}
          <button
            onClick={() => setLang(l => l === "en" ? "hi" : "en")}
            className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 hover:text-white bg-white/8 hover:bg-white/15 px-2.5 py-1.5 rounded-lg transition-all border border-white/10"
          >
            <Globe className="h-3 w-3" />
            {lang === "en" ? "हिंदी" : "EN"}
          </button>

          {/* Mobile Menu Toggle */}
          <button
            className="md:hidden text-white p-1.5 rounded-lg hover:bg-white/10 transition-all"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden border-t border-white/10 bg-slate-900/95 absolute top-16 left-0 w-full shadow-2xl backdrop-blur-md">
          <nav className="flex flex-col p-3 gap-1">
            {links.map(link => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  pathname === link.href
                    ? "text-white bg-orange-500/20 border border-orange-500/30"
                    : "text-slate-300 hover:text-white hover:bg-white/5"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </header>
  )
}
