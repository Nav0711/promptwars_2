"use client"

import { useState, useRef, useEffect } from "react"
import { MessageCircle, X, Send, Globe, ExternalLink, ThumbsUp, ThumbsDown } from "lucide-react"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"

type Message = {
  role: "user" | "assistant"
  content: string
  sources?: string[]
  guardrail_triggered?: boolean
  latency_ms?: number
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

const INITIAL_SUGGESTIONS_EN = [
  "Where is my polling booth?",
  "What is NOTA?",
  "How do I register as a voter?",
  "What documents do I need on election day?",
]

const INITIAL_SUGGESTIONS_HI = [
  "मेरा मतदान केंद्र कहाँ है?",
  "NOTA क्या है?",
  "मतदाता पंजीकरण कैसे करें?",
  "चुनाव के दिन कौन से दस्तावेज़ चाहिए?",
]

export function ChatWidget() {
  const [isOpen, setIsOpen]       = useState(false)
  const [language, setLanguage]   = useState<"en" | "hi">("en")
  const [messages, setMessages]   = useState<Message[]>([
    {
      role: "assistant",
      content: "Namaste! I am Chunav Saathi, your neutral Indian election information assistant. How can I help you today?",
    },
  ])
  const [suggestions, setSuggestions] = useState<string[]>(INITIAL_SUGGESTIONS_EN)
  const [input, setInput]         = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const bottomRef                 = useRef<HTMLDivElement>(null)
  const inputRef                  = useRef<HTMLInputElement>(null)

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isLoading])

  // Focus trap / A11y
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus()
    }
  }, [isOpen])

  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) setIsOpen(false)
    }
    window.addEventListener("keydown", handleEsc)
    return () => window.removeEventListener("keydown", handleEsc)
  }, [isOpen])

  // Switch language greeting
  const toggleLanguage = () => {
    const newLang = language === "en" ? "hi" : "en"
    setLanguage(newLang)
    setSuggestions(newLang === "hi" ? INITIAL_SUGGESTIONS_HI : INITIAL_SUGGESTIONS_EN)
    setMessages([{
      role: "assistant",
      content: newLang === "hi"
        ? "नमस्ते! मैं चुनाव साथी हूँ। आज मैं आपकी कैसे मदद कर सकता हूँ?"
        : "Namaste! I am Chunav Saathi, your neutral Indian election information assistant. How can I help you today?",
    }])
  }

  const sendMessage = async (text: string) => {
    if (!text.trim()) return

    setInput("")
    setMessages(prev => [...prev, { role: "user", content: text }])
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE}/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: `session-${Date.now()}`,
          message:    text,
          language:   language,
        }),
      })

      if (!response.ok) throw new Error(`HTTP ${response.status}`)

      const data = await response.json()

      setMessages(prev => [...prev, {
        role:               "assistant",
        content:            data.response,
        sources:            data.sources || [],
        guardrail_triggered: data.guardrail_triggered,
        latency_ms:         data.latency_ms,
      }])

      if (data.suggestions?.length) {
        setSuggestions(data.suggestions)
      }
    } catch (error) {
      console.error(error)
      setMessages(prev => [...prev, {
        role: "assistant",
        content: language === "hi"
          ? "मुझे खेद है, अभी सर्वर से कनेक्ट नहीं हो पा रहा। कृपया बाद में पुनः प्रयास करें।"
          : "I'm having trouble connecting to the server. Please try again later.",
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      {/* Floating Trigger Button */}
      {!isOpen && (
        <Button
          id="chunav-chat-open-btn"
          onClick={() => setIsOpen(true)}
          aria-label="Open Chunav Saathi Chat"
          className="fixed bottom-6 right-6 h-16 w-16 rounded-full shadow-2xl shadow-orange-500/40 bg-gradient-to-br from-orange-500 via-amber-500 to-orange-600 hover:scale-110 transition-all duration-300 z-50"
        >
          <MessageCircle className="h-7 w-7 text-white" />
          <span className="absolute -top-1 -right-1 flex h-4 w-4">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-4 w-4 bg-green-500"></span>
          </span>
        </Button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <Card
          id="chunav-chat-window"
          role="region"
          aria-label="Chunav Saathi Chat Window"
          className="fixed bottom-0 right-0 sm:bottom-6 sm:right-6 w-full sm:w-[380px] h-[85vh] sm:h-[560px] flex flex-col shadow-2xl border border-orange-500/20 bg-slate-900 sm:rounded-2xl rounded-t-2xl overflow-hidden z-50 animate-in slide-in-from-bottom-5"
        >
          {/* Header */}
          <CardHeader className="bg-gradient-to-r from-orange-600 to-amber-500 py-3 px-4 flex flex-row justify-between items-center text-white shrink-0">
            <CardTitle className="text-sm font-semibold flex items-center gap-2">
              <MessageCircle className="h-4 w-4" />
              Chunav Saathi
              <span className="text-xs font-normal opacity-80 hidden sm:inline">
                {language === "hi" ? "| हिंदी" : "| English"}
              </span>
            </CardTitle>
            <div className="flex items-center gap-1">
              {/* Language Toggle */}
              <Button
                id="chunav-lang-toggle"
                variant="ghost"
                size="sm"
                onClick={toggleLanguage}
                aria-label={language === "en" ? "Switch to Hindi language" : "Switch to English language"}
                className="h-7 px-2 text-xs text-white hover:bg-white/20 hover:text-white font-medium"
                title="Switch language"
              >
                <Globe className="h-3 w-3 mr-1" />
                {language === "en" ? "हिंदी" : "English"}
              </Button>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Close chat"
                className="h-7 w-7 text-white hover:bg-white/20 hover:text-white"
                onClick={() => setIsOpen(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>

          {/* Suggestion Chips */}
          <div className="flex gap-2 px-3 py-2 bg-slate-800/80 overflow-x-auto shrink-0 border-b border-slate-700/50 scrollbar-none">
            {suggestions.slice(0, 3).map((s, i) => (
              <button
                key={i}
                onClick={() => sendMessage(s)}
                className="whitespace-nowrap text-xs px-3 py-1.5 rounded-full border border-orange-500/40 text-orange-300 hover:bg-orange-500/20 hover:border-orange-500 transition-all duration-200 shrink-0"
              >
                {s}
              </button>
            ))}
          </div>

          {/* Messages */}
          <CardContent className="flex-1 p-0 overflow-hidden">
            <ScrollArea className="h-full p-4" aria-live="polite">
              <div className="flex flex-col gap-4">
                {messages.map((msg, i) => (
                  <div key={i} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}>
                    <div
                      className={`max-w-[88%] rounded-2xl p-3 text-sm leading-relaxed ${
                        msg.role === "user"
                          ? "bg-orange-500 text-white rounded-br-sm"
                          : "bg-slate-800 text-slate-100 rounded-bl-sm border border-slate-700/60"
                      }`}
                    >
                      {msg.content}
                    </div>

                    {/* Sources */}
                    {msg.role === "assistant" && msg.sources && msg.sources.length > 0 && (
                      <div className="mt-1 flex flex-wrap gap-1">
                        {msg.sources.map((src, si) => (
                          <a
                            key={si}
                            href={src}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[10px] text-orange-400 hover:text-orange-300 flex items-center gap-1 underline underline-offset-2"
                          >
                            <ExternalLink className="h-2.5 w-2.5" />
                            {new URL(src).hostname.replace("www.", "")}
                          </a>
                        ))}
                      </div>
                    )}

                    {/* Feedback row for assistant messages */}
                    {msg.role === "assistant" && i > 0 && (
                      <div className="flex items-center gap-2 mt-1">
                        {msg.latency_ms && (
                          <span className="text-[10px] text-slate-500">{msg.latency_ms}ms</span>
                        )}
                        <button className="text-slate-500 hover:text-green-400 transition-colors" aria-label="Mark as helpful" title="Helpful">
                          <ThumbsUp className="h-3 w-3" aria-hidden="true" />
                        </button>
                        <button className="text-slate-500 hover:text-red-400 transition-colors" aria-label="Mark as not helpful" title="Not helpful">
                          <ThumbsDown className="h-3 w-3" aria-hidden="true" />
                        </button>
                        {msg.guardrail_triggered && (
                          <span className="text-[10px] text-amber-500 bg-amber-500/10 px-1.5 py-0.5 rounded">🛡️ Guardrail</span>
                        )}
                      </div>
                    )}
                  </div>
                ))}

                {/* Typing Indicator */}
                {isLoading && (
                  <div className="flex justify-start" aria-label="Assistant is typing">
                    <div className="bg-slate-800 border border-slate-700/60 rounded-2xl rounded-bl-sm p-3 flex gap-1.5 items-center">
                      <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                      <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: "0.4s" }} />
                    </div>
                  </div>
                )}
                <div ref={bottomRef} />
              </div>
            </ScrollArea>
          </CardContent>

          {/* Input */}
          <CardFooter className="p-3 bg-slate-800/80 border-t border-slate-700/50 shrink-0">
            <form
              onSubmit={(e) => { e.preventDefault(); sendMessage(input) }}
              className="flex w-full gap-2 items-center"
            >
              <Input
                id="chunav-chat-input"
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={language === "hi" ? "चुनाव के बारे में पूछें..." : "Ask about elections..."}
                disabled={isLoading}
                className="flex-1 bg-slate-700 border-slate-600 text-slate-100 placeholder:text-slate-400 focus-visible:ring-orange-500"
              />
              <Button
                id="chunav-chat-send-btn"
                type="submit"
                size="icon"
                aria-label="Send message"
                disabled={isLoading || !input.trim()}
                className="bg-orange-500 hover:bg-orange-600 text-white shrink-0 h-10 w-10"
              >
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </CardFooter>
        </Card>
      )}
    </>
  )
}
