import type { Metadata } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/Navbar";
import { ErrorBoundary } from "@/components/ErrorBoundary";

const fontSans = Plus_Jakarta_Sans({
  variable: "--font-sans",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Chunav Saathi - Election Intelligence Hub",
  description: "AI-powered election intelligence platform for India. Real-time election schedules, voter awareness tools, and AI-powered civic assistance.",
  keywords: "India elections, voter registration, polling booth, NOTA, ECI, Chunav Saathi",
  openGraph: {
    title: "Chunav Saathi — India Election Intelligence",
    description: "AI-powered election intelligence for the world's largest democracy.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${fontSans.variable} font-sans h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-950 text-slate-50 selection:bg-orange-500/30">
        {/* Skip to content — accessibility */}
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-orange-500 focus:text-white focus:rounded-lg focus:text-sm focus:font-semibold focus:outline-none focus:ring-2 focus:ring-white"
        >
          Skip to main content
        </a>
        <Navbar />
        <ErrorBoundary>
          <div id="main-content" role="main">
            {children}
          </div>
        </ErrorBoundary>
      </body>
    </html>
  );
}
