"use client"

import { Component, ErrorInfo, ReactNode } from "react"
import { AlertTriangle, RefreshCcw } from "lucide-react"

interface Props {
  children?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center p-6 text-center" role="alert" aria-live="assertive">
          <div className="w-16 h-16 rounded-full bg-red-500/10 flex items-center justify-center mb-6">
            <AlertTriangle className="w-8 h-8 text-red-500" aria-hidden="true" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-3">Something went wrong</h2>
          <p className="text-slate-400 max-w-md mb-8">
            An unexpected error occurred while rendering this page. Our team has been notified.
          </p>
          <button
            onClick={() => {
              this.setState({ hasError: false })
              window.location.reload()
            }}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-800 text-white font-medium hover:bg-slate-700 transition-colors focus:outline-none focus:ring-2 focus:ring-orange-500"
            aria-label="Try reloading the page"
          >
            <RefreshCcw className="w-4 h-4" aria-hidden="true" />
            Try again
          </button>
        </div>
      )
    }

    return this.props.children
  }
}
