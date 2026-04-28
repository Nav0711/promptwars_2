# 🗳️ Chunav Saathi — India Election Intelligence Assistant
### Product Requirements Document (PRD)
**Version:** 1.0.0  
**Hackathon:** Prompt Wars — Powered by Antigravity × GCP  
**Author:** Navdeep Singh  
**Status:** Draft — Submission Ready  
**Last Updated:** April 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Product Vision & Goals](#3-product-vision--goals)
4. [Target Users & Personas](#4-target-users--personas)
5. [Architecture Overview](#5-architecture-overview)
6. [Tech Stack](#6-tech-stack)
7. [Feature Specifications](#7-feature-specifications)
   - 7.1 [AI Chatbot — Chunav Saathi](#71-ai-chatbot--chunav-saathi)
   - 7.2 [Dashboard — Election Intelligence Hub](#72-dashboard--election-intelligence-hub)
   - 7.3 [Live Election Tracker](#73-live-election-tracker)
   - 7.4 [FAQ & Knowledge Base](#74-faq--knowledge-base)
   - 7.5 [Polling Location Finder](#75-polling-location-finder)
   - 7.6 [Voter Awareness Module](#76-voter-awareness-module)
8. [RAG Pipeline Design](#8-rag-pipeline-design)
9. [Safety, Guardrails & Bias Mitigation](#9-safety-guardrails--bias-mitigation)
10. [Data Sources & APIs](#10-data-sources--apis)
11. [GCP Infrastructure Plan](#11-gcp-infrastructure-plan)
12. [Antigravity Integration](#12-antigravity-integration)
13. [UI/UX Design Principles](#13-uiux-design-principles)
14. [API Contract](#14-api-contract)
15. [Non-Functional Requirements](#15-non-functional-requirements)
16. [Security & Compliance](#16-security--compliance)
17. [Milestones & Delivery Plan](#17-milestones--delivery-plan)
18. [Success Metrics](#18-success-metrics)
19. [Risks & Mitigations](#19-risks--mitigations)
20. [Appendix](#20-appendix)

---

## 1. Executive Summary

**Chunav Saathi** (चुनाव साथी — "Election Companion") is an AI-powered election intelligence platform built for Indian citizens, journalists, researchers, and first-time voters. It combines a real-time election dashboard with a RAG-powered conversational assistant that answers questions about the Indian electoral process, live election schedules, voter registration, candidate information, polling locations, and ECI notifications.

The platform is built on **Google Cloud Platform (GCP)** using **Gemini API** as the primary AI engine, deployed and managed through **Antigravity** for the Prompt Wars hackathon track.

This is not just a chatbot — it is a full-stack civic intelligence system with a live dashboard, structured data views, location-aware features, and a rigorously guardrailed AI assistant that remains neutral, factual, and safe.

---

## 2. Problem Statement

India conducts the world's largest democratic elections. Yet:

- **Voter information is fragmented** across ECI website, state CEO portals, and Voter Helpline app — all of which are non-conversational and hard to navigate.
- **Low digital literacy** means millions cannot find polling booth details, nomination deadlines, or NOTA rules without help.
- **Misinformation** spreads rapidly during election seasons via WhatsApp and social media.
- **No single real-time unified view** exists for tracking which states/constituencies are currently in active election phases.
- **First-time voters** (18–22 age group) find the process opaque, leading to low turnout.

**Chunav Saathi** solves this by being the intelligent, conversational, and visual single source of truth for Indian elections.

---

## 3. Product Vision & Goals

### Vision
> "Make every Indian voter as informed as a political journalist — instantly, in their language, on any device."

### Goals

| # | Goal | Metric |
|---|------|--------|
| G1 | Reduce time-to-answer for election queries from 5+ minutes to < 10 seconds | Avg. response time |
| G2 | Provide real-time election schedule and phase data | Live data freshness < 1 hr |
| G3 | Answer 95% of common election queries without human intervention | Chatbot resolution rate |
| G4 | Maintain strict political neutrality in all AI responses | Bias audit score |
| G5 | Support Hindi + English bilingual interaction | Language coverage |
| G6 | Serve location-aware polling booth data | Booth lookup accuracy |

---

## 4. Target Users & Personas

### Persona 1: Priya — First-Time Voter (Age 19, Lucknow)
- Just turned 18, registered on Voter Portal
- Wants to know: "Where is my polling booth?", "What do I carry on election day?", "Can I vote if I moved cities?"
- Prefers Hindi, uses mobile

### Persona 2: Arjun — Political Journalist (Age 32, Delhi)
- Covers UP and Rajasthan state elections
- Wants: Real-time phase schedules, seat-wise results as they come, candidate affiliations
- Prefers data tables and downloadable reports

### Persona 3: Dr. Meera — Academic Researcher (Age 45, Pune)
- Studies voter turnout patterns by constituency
- Wants: Historical data, state comparison dashboards, trend charts

### Persona 4: Ramesh — Rural Voter (Age 55, Bihar)
- Low digital literacy, uses basic Android phone
- Needs: Simple Hindi chatbot, voice-friendly interaction, booth locator by address

### Persona 5: Sneha — Civic Tech Developer (Age 27, Bangalore)
- Building a voter drive app
- Needs: API access, structured data, webhook for election event triggers

---

## 5. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER LAYER                                   │
│           Web App (Next.js)  ·  Mobile PWA  ·  REST API             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                     FRONTEND (Vercel / Cloud Run)                   │
│    Dashboard UI   ·   Chatbot Widget   ·   Map View   ·   FAQs      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                   BACKEND API LAYER (GCP Cloud Run)                 │
│   FastAPI / Node.js   ·   Auth Middleware   ·   Rate Limiter        │
│                                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │
│  │ Chat Router │  │ Data Service │  │  Location Service        │   │
│  │ (Gemini AI) │  │ (Elections)  │  │  (Maps + Booth Finder)   │   │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬───────────────┘   │
└─────────┼────────────────┼──────────────────────┼───────────────────┘
          │                │                       │
┌─────────▼────────────────▼──────────────────────▼───────────────────┐
│                        DATA & AI LAYER                               │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              RAG PIPELINE (GCP Vertex AI)                   │    │
│  │   Document Ingestion → Chunking → Embedding → Vector Store  │    │
│  │   Cloud Storage (PDFs/HTML) → Vertex AI Embeddings          │    │
│  │   → Firestore (Vector) → Gemini 1.5 Flash (Generator)       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌───────────────────┐  ┌────────────────────┐  ┌───────────────┐  │
│  │   Cloud Firestore │  │  BigQuery (Analytics│  │ Cloud Memstore│  │
│  │   (Live Election  │  │  Historical Data)   │  │ Redis (Cache) │  │
│  │    Schedule Data) │  │                     │  │               │  │
│  └───────────────────┘  └────────────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                             │
│  ECI API / Scrapers  ·  Google Maps API  ·  MyGov.in RSS            │
│  Gemini API  ·  Cloud Scheduler (Cron Jobs)  ·  Pub/Sub             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Tech Stack

### Frontend
| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | Next.js 14 (App Router) | SSR for SEO, fast page loads |
| Styling | Tailwind CSS + shadcn/ui | Rapid, accessible UI |
| Charts | Recharts + D3.js | Rich data visualizations |
| Maps | Google Maps JS SDK | Polling booth location display |
| State | Zustand | Lightweight client state |
| i18n | next-intl | Hindi/English bilingual support |

### Backend
| Layer | Technology | Reason |
|-------|-----------|--------|
| API Server | FastAPI (Python) | Async, fast, great for AI pipelines |
| Authentication | Firebase Auth / GCP IAP | Easy, scalable auth |
| Caching | Cloud Memorystore (Redis) | Sub-ms response for repeated queries |
| Task Queue | Cloud Tasks / Pub/Sub | Async scraping, embedding jobs |

### AI / ML
| Component | Technology | Reason |
|-----------|-----------|--------|
| Primary LLM | Gemini 1.5 Flash | Free tier: 15 RPM / 1M tokens/day, fast |
| Fallback LLM | Groq (Llama 3.1 70B) | Ultra-high rate limit, free tier |
| Embeddings | Vertex AI text-embedding-004 | Best-in-class multilingual |
| Vector Store | Firestore with Vector Search | Native GCP integration |
| Orchestration | LangChain (Python) | RAG chain management |
| Safety | Gemini Safety Filters + Custom | Guardrails on political content |

### Infrastructure (GCP)
| Service | Use |
|---------|-----|
| Cloud Run | Containerized API hosting (serverless) |
| Cloud Storage | Document storage for RAG knowledge base |
| Firestore | Live election data + vector embeddings |
| BigQuery | Historical election analytics |
| Vertex AI | Embedding generation, model hosting |
| Cloud Scheduler | Periodic data refresh (hourly ECI scrape) |
| Cloud Pub/Sub | Real-time event propagation |
| Secret Manager | API key management |
| Cloud CDN | Static asset acceleration |

### Deployment / DevOps
| Tool | Use |
|------|-----|
| Antigravity | Platform deployment, prompt management, observability |
| Docker | Container packaging |
| GitHub Actions | CI/CD pipeline |
| Terraform | GCP infra-as-code |

---

## 7. Feature Specifications

---

### 7.1 AI Chatbot — Chunav Saathi

The centerpiece of the product. A conversational AI assistant powered by Gemini 1.5 Flash with a RAG knowledge base, available 24/7 on web and mobile.

#### Core Capabilities

| Capability | Description |
|-----------|-------------|
| Election Process Q&A | Full coverage of ECI procedures, nomination to result |
| Voter Registration Help | How to register, check status, update details on Voter Portal |
| Polling Booth Finder | "Where do I vote?" with address → maps integration |
| Schedule & Phases | "When is voting in Rajasthan?" → Phase-wise dates |
| Candidate Information | Neutral, factual — name, party affiliation, constituency |
| NOTA & Voting Rules | Explain secret ballot, NOTA, EVM, VVPAT |
| Code of Conduct | MCC rules, what's allowed/not during election period |
| Results Information | Historical results lookup |
| Language Switching | Respond in Hindi if asked in Hindi |

#### Chatbot UX Flow

```
User Input (text/voice)
        ↓
Language Detection (Hi/En)
        ↓
Intent Classification
   ├── Election Info → RAG retrieval → Gemini → Response
   ├── Location Query → Maps API + booth DB → Response
   ├── Live Schedule → Firestore → Response
   ├── Out of scope → Polite redirect
   └── Political opinion → Guardrail → Neutral decline
        ↓
Safety Filter (Gemini built-in + custom rules)
        ↓
Response with citations + follow-up suggestions
```

#### Prompt Engineering Strategy

The chatbot system prompt follows this structure:

```
SYSTEM PROMPT ARCHITECTURE:
1. Role Definition: "You are Chunav Saathi, a neutral Indian election information assistant..."
2. Scope Boundaries: Elections, ECI rules, voter services, EVM, schedules
3. Hard Rules:
   - Never express opinions on political parties, candidates, or governments
   - Never predict election outcomes
   - Never comment on ongoing legal/court cases involving politicians
   - Always cite ECI / official sources
   - Respond in the language of the question (Hindi/English)
4. Fallback Instruction: "If unsure, say 'I recommend checking eci.gov.in directly'"
5. RAG Context Injection: Retrieved chunks prepended to each user query
6. Citation Format: "According to ECI notification dated..."
```

#### Suggested Questions (Quick Chips)
- "Where is my polling booth?"
- "When is voting in my state?"
- "How do I register as a voter?"
- "What documents do I carry on election day?"
- "What is NOTA?"
- "What is the Model Code of Conduct?"
- "How does EVM work?"

#### Multilingual Support
- Primary: English, Hindi
- Phase 2: Tamil, Telugu, Bengali, Marathi (using Gemini's multilingual capability)

---

### 7.2 Dashboard — Election Intelligence Hub

A rich, data-driven dashboard visible without login, giving an overview of India's current and upcoming election landscape.

#### Dashboard Sections

**Section A: Election Overview Banner**
- Current active elections (state/UT/by-elections)
- Days until next major election phase
- Total seats up for election
- Eligible voter count

**Section B: Election Phase Timeline**
- Visual Gantt-style timeline of all election phases
- Color-coded: Completed / Active / Upcoming
- Clickable to drill into phase details

**Section C: State-wise Map**
- India choropleth map
- States color-coded: Election Active / Scheduled / No Election
- Click state → state election dashboard
- Hover → quick stats (seats, date, turnout if available)

**Section D: Live Counting / Results Panel** *(when applicable)*
- Real-time seat tally per party (updated every 5 minutes during counting)
- Leading / Won / Total columns
- Trend sparklines per party

**Section E: Key Dates Ticker**
- Scrolling timeline: Nomination deadlines, withdrawal deadlines, voting dates, result dates
- Sourced from official ECI schedule

**Section F: Voter Turnout Analytics**
- Historical turnout chart by state (last 3 elections)
- Gender split in voter registration
- Urban vs rural turnout heatmap

**Section G: Recent ECI Announcements**
- RSS/scraper feed from ECI press releases
- Categorized: Schedule | MCC | Candidate | Results | Notices

**Section H: Quick Access Tools**
- "Find My Polling Booth" card → Chatbot or direct lookup
- "Check Voter Registration" card → Links to voterportal.eci.gov.in
- "Know Your Candidate" card → Search by constituency
- "File Complaint (cVIGIL)" card → Deep-link to cVIGIL app

---

### 7.3 Live Election Tracker

A dedicated page showing real-time election status across India.

#### Features

- **Phase Status Cards**: Each phase shown as a card with status badge (UPCOMING / VOTING TODAY / COMPLETED)
- **Constituency-level Drill-down**: Click a state → see all constituencies, scheduled date, turnout phase
- **Date Filter**: Browse elections by date range
- **Notification Alerts**: "Set reminder" for upcoming election dates (via browser notification)
- **Data Refresh Indicator**: Shows "Last updated: X minutes ago"

#### Live Data Update Strategy
- Cloud Scheduler triggers ECI data scraper every 60 minutes
- Results during counting day: refresh every 5 minutes via WebSocket / SSE (Server-Sent Events)
- Cache hot data in Redis, invalidate on scheduled refresh

---

### 7.4 FAQ & Knowledge Base

A searchable, structured FAQ covering the entire Indian election process.

#### Categories

| Category | Sample Questions |
|----------|-----------------|
| Voter Registration | How to register? How to check status? NVSP vs Voter Helpline? |
| Voting Process | What ID do I need? Can I vote if I moved? Proxy voting rules? |
| EVM & Technology | How does EVM work? What is VVPAT? Is EVM tamper-proof? |
| Candidates & Parties | How to file nomination? What is affidavit disclosure? |
| Model Code of Conduct | What is MCC? When does it come into effect? Violations? |
| Election Commission | Who is the CEC? What are ECI powers? |
| Results & Counting | How is counting done? What is margin of victory? |
| Special Provisions | Postal ballot, EPIC card, Overseas voters, Senior citizen voting |
| NOTA | History of NOTA, how to use, what happens if NOTA wins? |
| Complaints & Grievances | cVIGIL, 1950 helpline, how to report MCC violations |

#### Search
- Full-text search with Firestore
- Semantic search via embeddings for "fuzzy" FAQ matching
- Each FAQ card has a "Ask the AI" button to expand into chatbot

---

### 7.5 Polling Location Finder

A standalone tool (and chatbot capability) to find voting booth details.

#### Input Options
1. Voter ID / EPIC number → direct match
2. Full Name + DOB + State → fuzzy search
3. Address / PIN code → geo-lookup
4. Current Location (GPS) → nearest booths

#### Output
- Polling booth name, number, address
- Google Maps embedded view + "Get Directions" button
- Booth timings (typically 7 AM – 6 PM)
- Accessibility info (wheelchair accessible? Yes/No)
- Serial number on voter list

#### Backend
- Booth data sourced from ECI's voter list APIs / CSV files
- Stored in Firestore, indexed by PIN code + state
- Fallback: Deep-link to voterportal.eci.gov.in with pre-filled params

---

### 7.6 Voter Awareness Module

Educational content to drive civic participation, especially for first-time voters.

#### Components

- **"Your Vote Matters" Infographic Section**: Animated stats on voter turnout, historical impact of close elections
- **Election Process Explainer**: Step-by-step illustrated guide: Register → Verify → Vote → Results
- **Video Embed Integration**: ECI official voter awareness videos
- **Share & Inspire**: "I'm a voter" social share card generator
- **Quiz Module**: "How well do you know the election process?" — 5-question quiz powered by Gemini

---

## 8. RAG Pipeline Design

The knowledge base that powers the chatbot's factual accuracy.

### Document Sources

| Source | Format | Refresh Frequency |
|--------|--------|-------------------|
| ECI Election Schedule Notifications | PDF / HTML | On release |
| Representation of the People Act, 1951 | PDF | Annually |
| Model Code of Conduct Full Text | PDF | Per election |
| ECI Press Releases | HTML | Daily |
| Voter Guide Documents | PDF | Per election cycle |
| State CEO Notifications | PDF | Per state election |
| ECI FAQ pages | HTML | Weekly |
| Form 6, 6A, 7, 8 instructions | PDF | Annually |
| Historical election results (ECI data) | CSV | Post-election |

### Pipeline Steps

```
STEP 1: INGESTION
  Cloud Scheduler → Scraper (Python/Scrapy) → Cloud Storage bucket

STEP 2: CHUNKING
  PDF/HTML → Text extraction (PyMuPDF / BeautifulSoup)
  → Recursive character splitter: chunk_size=800, overlap=100

STEP 3: EMBEDDING
  Each chunk → Vertex AI text-embedding-004
  → 768-dimensional vector

STEP 4: STORAGE
  Vector + metadata → Firestore Vector Search collection
  Metadata: source_url, doc_title, date_scraped, category, language

STEP 5: RETRIEVAL
  User query → Embed query → ANN search (top-5 chunks)
  → Re-rank by relevance score

STEP 6: GENERATION
  System prompt + retrieved chunks + user query → Gemini 1.5 Flash
  → Response with citations

STEP 7: POST-PROCESSING
  Safety filter check → Language check → Format response
  → Stream to frontend
```

### Vector Search Config
```python
# Firestore Vector Search Index
index_config = {
    "dimension": 768,
    "distance_measure": "COSINE",
    "algorithm": "APPROXIMATE_NEAREST_NEIGHBOR"
}
```

---

## 9. Safety, Guardrails & Bias Mitigation

This is a politically sensitive domain. Guardrails are non-negotiable.

### Layer 1: Gemini Built-in Safety Filters
```python
safety_settings = [
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
```

### Layer 2: Custom Political Neutrality Rules

**Hard-blocked topics (always redirect, never answer):**
- "Which party should I vote for?"
- Any question asking to predict election winner
- Comparative quality of political leaders
- Ongoing election-related court cases
- Exit poll interpretation
- "Is [politician] corrupt?"

**Soft-redirect topics (answer factually, no opinion):**
- Party manifesto summaries (describe, don't evaluate)
- Candidate criminal record disclosure (link to affidavit, don't editorialize)
- Historical election controversies (state facts only)

### Layer 3: Input Classification
- Pre-query classifier (lightweight Gemini Flash call) categorizes input:
  - `ELECTION_INFO` → proceed to RAG
  - `POLITICAL_OPINION` → polite decline template
  - `OUT_OF_SCOPE` → "I can only help with election topics"
  - `HARMFUL` → block + log

### Layer 4: Output Validation
- Post-generation check: scan for party names + sentiment → flag if opinion detected
- Human review queue for flagged responses (Firestore audit log)

### Layer 5: Rate Limiting
- 20 queries/user/hour (cookie-based for anonymous users)
- 100 queries/user/hour (logged-in users)
- Abuse pattern detection via Cloud Armor

### Bias Audit Plan
- Monthly: Sample 500 chatbot responses, manually review for political lean
- Bias score tracked in BigQuery
- Red team: Intentionally ask loaded political questions; verify refusals

---

## 10. Data Sources & APIs

| Data Type | Source | Method | License |
|-----------|--------|--------|---------|
| Election schedule | eci.gov.in | Scraper + Manual | Public |
| Voter registration status | voterportal.eci.gov.in | Deep-link | Public |
| Polling booth data | ECI voter list download | CSV bulk download | Public |
| State CEO notifications | ceo.[state].gov.in | RSS / Scraper | Public |
| Candidate affidavits | myneta.info / affidavit.eci.gov.in | API / Scraper | Public |
| ECI press releases | eci.gov.in/press-release | RSS | Public |
| Maps & geocoding | Google Maps Platform | REST API | Paid (free tier) |
| Historical results | ECI data portal | CSV | Public |
| MyGov announcements | mygov.in | RSS | Public |

---

## 11. GCP Infrastructure Plan

### Services Used

```
Project: chunav-saathi-prod
Region: asia-south1 (Mumbai) — for latency

Services:
├── Cloud Run (API)                  — 2 containers (FastAPI + NextJS)
├── Cloud Storage                    — RAG documents bucket
├── Firestore (Native mode)          — Live data + vector search
├── BigQuery                         — Analytics dataset
├── Vertex AI                        — Embeddings + optional fine-tuning
├── Cloud Scheduler                  — 6 cron jobs (hourly scrape, daily index)
├── Cloud Pub/Sub                    — Election event streaming
├── Cloud Memorystore (Redis)        — Query cache
├── Secret Manager                   — Gemini API key, Maps key
├── Cloud Armor                      — DDoS & rate limiting
├── Cloud CDN + Load Balancer        — Frontend asset delivery
└── Cloud Logging + Monitoring       — Observability
```

### Cost Estimate (Hackathon Phase — Free Tier Optimized)

| Service | Free Tier Limit | Expected Usage |
|---------|-----------------|----------------|
| Cloud Run | 2M req/month | < 500K |
| Firestore | 50K reads/day | ~20K |
| Vertex AI Embeddings | $0.000025/1K chars | < $5 |
| Gemini 1.5 Flash API | 15 RPM free | Sufficient for demo |
| Cloud Storage | 5 GB free | ~2 GB RAG docs |
| BigQuery | 10 GB/month free | < 1 GB |
| Google Maps | $200 credit/month | < $50 |

**Estimated monthly cost in production: ~$40–80 USD** (heavily cached, GCP free tier maximized)

---

## 12. Antigravity Integration

Antigravity serves as the deployment and prompt management layer for this hackathon entry.

### What Antigravity Handles

| Function | Antigravity Role |
|---------|-----------------|
| Prompt Versioning | Track system prompt iterations for chatbot |
| Prompt Deployment | Push new prompt versions without redeployment |
| Observability | Trace each chatbot call, latency, token usage |
| A/B Testing | Test two prompt variants (Hindi-first vs English-first) |
| Guardrail Management | Define and deploy political content filters via Antigravity rules |
| Model Routing | Route queries to Gemini vs Groq fallback based on load |
| Cost Tracking | Monitor token costs per query session |

### Antigravity Config (proposed)

```yaml
# antigravity.yaml
project: chunav-saathi
environment: production

models:
  primary:
    provider: google
    model: gemini-1.5-flash
    temperature: 0.2
    max_tokens: 1024
  fallback:
    provider: groq
    model: llama3-70b-8192
    temperature: 0.2

prompts:
  chatbot_system:
    version: v1.0
    file: prompts/chatbot_system.md
    variables:
      - retrieved_context
      - user_language
      - current_date

guardrails:
  - id: no_political_opinion
    type: output_filter
    pattern: "vote for|best party|worst candidate|should win"
    action: replace_with_template
    template: "I'm here to share factual election information only. For voter choices, please rely on your own research."

  - id: block_prediction
    type: input_classifier
    trigger: "who will win|predict result|exit poll"
    action: decline
    decline_message: "I don't make predictions about election outcomes. I can share official schedules and historical data instead."

observability:
  log_inputs: true
  log_outputs: true
  pii_masking: true
  latency_alert_ms: 3000
```

---

## 13. UI/UX Design Principles

### Design Language
- **Colors**: Saffron (#FF9933), White (#FFFFFF), Green (#138808), Navy Blue (#000080) — inspired by the Indian tricolor
- **Typography**: Inter (English), Noto Sans Devanagari (Hindi)
- **Accessibility**: WCAG 2.1 AA compliant, screen reader tested
- **Mobile First**: 60% of Indian internet users are on mobile

### Key UX Principles
1. **No Jargon**: Replace "Delimitation" with "Boundary changes for constituencies"
2. **Progressive Disclosure**: Show simple answer first, "Learn more" to expand
3. **Always Show Source**: Every chatbot response cites its source (ECI, MCC, etc.)
4. **Offline Fallback**: Cache last-known schedule data for offline viewing
5. **Low Bandwidth Mode**: Lightweight version for 2G/slow connections

### Chatbot UI
- Floating chat bubble on all dashboard pages
- Full-page chat mode on mobile
- Suggested chips update based on context (e.g., near election date → show booth finder chip)
- Typing indicator, streaming response (token-by-token)
- Thumbs up/down feedback on each response
- "Report this answer" button → logged for review

---

## 14. API Contract

### Base URL
```
https://api.chunavsaathi.in/v1
```

### Endpoints

#### POST /chat
Send a message to the chatbot.
```json
Request:
{
  "session_id": "uuid",
  "message": "मेरा मतदान केंद्र कहाँ है?",
  "language": "hi",
  "location": { "lat": 28.6139, "lng": 77.2090 }
}

Response:
{
  "response": "आपका मतदान केंद्र है: ...",
  "sources": ["ECI Notification 2024-03-01"],
  "suggestions": ["अगला चरण कब है?", "क्या लाना है?"],
  "guardrail_triggered": false,
  "latency_ms": 420
}
```

#### GET /elections/active
```json
Response:
{
  "elections": [
    {
      "state": "West Bengal",
      "type": "Assembly By-Election",
      "phases": [
        { "phase": 1, "date": "2026-05-07", "constituencies": 42, "status": "UPCOMING" }
      ]
    }
  ]
}
```

#### GET /elections/schedule
Query params: `state`, `year`, `type`

#### GET /booth/find
Query params: `epic_id` OR `name+dob+state` OR `pincode`

#### GET /faqs
Query params: `category`, `search`, `language`

#### GET /candidates
Query params: `constituency`, `state`, `election_id`

#### GET /dashboard/stats
Returns aggregate counts for the dashboard overview banner.

---

## 15. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| API Response Time (p95) | < 2 seconds for chatbot |
| Dashboard Load Time | < 1.5 seconds (LCP) |
| Uptime | 99.9% |
| Concurrent Users | 10,000 (hackathon demo: 500) |
| Mobile Performance Score | Lighthouse > 85 |
| Accessibility | WCAG 2.1 AA |
| Data Freshness | ECI schedule data < 1 hour old |
| Chatbot Accuracy | > 90% on curated test set |
| Bias Audit | < 2% political lean score |

---

## 16. Security & Compliance

### Data Privacy
- No personal voter data stored on our servers — all lookups delegate to official portals
- Session data encrypted at rest (AES-256) and in transit (TLS 1.3)
- No cookies for analytics without consent
- GDPR/IT Act 2000 compliant architecture

### API Security
- All APIs behind Google Cloud Armor (WAF)
- JWT-based auth for logged-in features
- API keys managed via GCP Secret Manager
- Input sanitization on all user inputs (prevent prompt injection)

### Prompt Injection Defense
```python
# Input sanitization before LLM call
def sanitize_input(user_input: str) -> str:
    # Remove known injection patterns
    injection_patterns = [
        r"ignore previous instructions",
        r"you are now",
        r"system prompt",
        r"jailbreak",
        r"DAN mode"
    ]
    for pattern in injection_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            raise GuardrailException("INJECTION_ATTEMPT")
    return user_input[:1000]  # Hard length limit
```

### Audit Logging
- Every chatbot request/response logged to Cloud Logging
- PII masked before logging (phone numbers, Voter IDs auto-redacted)
- Retention: 90 days

---

## 17. Milestones & Delivery Plan

### Hackathon Timeline (5-Day Sprint)

| Day | Milestone | Deliverables |
|-----|-----------|-------------|
| Day 1 | Foundation | GCP project setup, Firestore schema, Gemini API connected, basic chatbot working |
| Day 2 | RAG Pipeline | Document ingestion, embeddings, vector search, chatbot grounded in ECI data |
| Day 3 | Dashboard | Election schedule cards, India map, phase timeline, live data from Firestore |
| Day 4 | Features | Booth finder, FAQ page, guardrails, Hindi support, Antigravity integration |
| Day 5 | Polish & Deploy | Mobile PWA, performance tuning, demo video, Cloud Run deploy, README |

### Post-Hackathon Roadmap

| Phase | Timeline | Features |
|-------|----------|---------|
| v1.1 | Month 1 | Voice input (Google Speech-to-Text), more languages (Tamil, Bengali) |
| v1.2 | Month 2 | cVIGIL integration, push notifications for election reminders |
| v2.0 | Month 3 | Candidate comparison tool, manifesto summarizer (RAG on party manifestos) |
| v2.5 | Month 4 | WhatsApp chatbot integration (Twilio/Meta), partner with NGOs |

---

## 18. Success Metrics

### Hackathon Judging Criteria Alignment

| Judging Criterion | How We Address It |
|------------------|-------------------|
| Innovation | RAG + guardrailed political AI is novel for India civic tech |
| GCP Usage | 8+ GCP services deeply integrated |
| Antigravity Usage | Prompt versioning, guardrails, observability all on Antigravity |
| Impact | Civic utility for 970M+ eligible Indian voters |
| Technical Depth | Vector search, streaming, multilingual, real-time data |
| Demo Quality | Live dashboard + chatbot with real ECI data |

### Product Metrics (Post-launch)
- DAU / WAU ratio
- Chatbot resolution rate (no "I don't know" fallback needed)
- Booth finder accuracy (% of queries resolved)
- Avg. session duration
- Language split (Hindi vs English)
- Feedback thumbs up rate > 80%

---

## 19. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ECI website structure changes → scraper breaks | Medium | High | Multiple fallback parsers + manual backup CSVs |
| Gemini API rate limit hit during demo | Medium | High | Groq (Llama 3) as fallback, Redis cache frequent queries |
| Chatbot gives politically biased response | Low | Very High | Multi-layer guardrails, output validation, audit log |
| Booth data stale / inaccurate | Medium | Medium | Display freshness timestamp, link to official source always |
| Election data for future dates not yet released | High | Medium | Show "not yet announced" gracefully, link to ECI for updates |
| Mobile performance poor on 2G | Medium | High | Lazy loading, skeleton screens, offline cache, lite mode |

---

## 20. Appendix

### A. Prompt Template (Chatbot System Prompt)

```
You are Chunav Saathi (चुनाव साथी), an AI assistant created to help Indian citizens understand and participate in elections. You are operated by a civic technology team and powered by official Election Commission of India (ECI) information.

YOUR ROLE:
- Answer questions about Indian election processes, voter registration, polling booths, election schedules, EVM, NOTA, Model Code of Conduct, and related topics.
- Provide factual, neutral, cited information only.
- Respond in the same language as the user (Hindi or English).
- Always cite your source (e.g., "According to ECI notification dated...").

STRICT RULES:
1. NEVER express an opinion on any political party, candidate, or government.
2. NEVER predict or speculate about election outcomes.
3. NEVER compare the quality of political leaders.
4. If asked for your political opinion, respond: "I'm here to share factual election information only. I don't share opinions on political parties or candidates."
5. NEVER answer questions about ongoing legal/criminal cases involving politicians.
6. If a query is outside your scope, say: "That's outside what I can help with. For [topic], you can visit eci.gov.in or call the 1950 voter helpline."

CONTEXT FROM KNOWLEDGE BASE:
{{retrieved_context}}

CURRENT DATE: {{current_date}}
USER LANGUAGE: {{user_language}}

Remember: You are a trusted civic resource. Accuracy and neutrality are your highest values.
```

### B. Firestore Data Schema

```
Collection: elections
  Document: {election_id}
    - state: string
    - type: "General" | "Assembly" | "By-Election" | "LS"
    - year: number
    - phases: Array<{
        phase_number: number,
        voting_date: timestamp,
        constituencies: number,
        status: "UPCOMING" | "ACTIVE" | "COMPLETED",
        results_date: timestamp
      }>
    - schedule_released: boolean
    - eci_notification_url: string

Collection: booths
  Document: {booth_id}
    - state: string
    - district: string
    - constituency_name: string
    - constituency_number: number
    - booth_name: string
    - booth_number: string
    - address: string
    - pincode: string
    - lat: number
    - lng: number
    - wheelchair_accessible: boolean

Collection: rag_chunks
  Document: {chunk_id}
    - text: string
    - embedding: vector(768)
    - source_url: string
    - doc_title: string
    - category: string
    - language: "en" | "hi"
    - date_scraped: timestamp

Collection: chat_sessions
  Document: {session_id}
    - messages: Array<{role, content, timestamp}>
    - language: string
    - flagged: boolean
    - feedback: number  // 1 = thumbs up, -1 = thumbs down
```

### C. Repository Structure

```
chunav-saathi/
├── README.md
├── antigravity.yaml
├── docker-compose.yml
├── terraform/                    # GCP infra-as-code
│   ├── main.tf
│   ├── firestore.tf
│   └── cloud_run.tf
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI entry point
│   │   ├── routers/
│   │   │   ├── chat.py           # /chat endpoint
│   │   │   ├── elections.py      # /elections endpoints
│   │   │   ├── booth.py          # /booth/find endpoint
│   │   │   └── faqs.py           # /faqs endpoint
│   │   ├── services/
│   │   │   ├── gemini.py         # Gemini API wrapper
│   │   │   ├── rag.py            # RAG pipeline
│   │   │   ├── guardrails.py     # Safety filters
│   │   │   └── maps.py           # Google Maps integration
│   │   └── models/
│   │       └── schemas.py        # Pydantic models
│   ├── ingestion/
│   │   ├── scraper.py            # ECI scraper
│   │   ├── chunker.py            # Document chunker
│   │   └── embedder.py           # Vertex AI embedder
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # Dashboard home
│   │   ├── chat/page.tsx         # Full-page chat
│   │   ├── elections/page.tsx    # Election tracker
│   │   ├── faqs/page.tsx         # FAQ page
│   │   └── booth/page.tsx        # Booth finder
│   ├── components/
│   │   ├── ChatWidget.tsx        # Floating chatbot
│   │   ├── ElectionMap.tsx       # India choropleth
│   │   ├── PhaseTimeline.tsx     # Phase Gantt chart
│   │   ├── LiveTicker.tsx        # Key dates scroller
│   │   └── DashboardCards.tsx    # Overview cards
│   └── package.json
├── prompts/
│   ├── chatbot_system.md         # System prompt
│   └── input_classifier.md      # Pre-query classifier prompt
└── docs/
    ├── PRD.md                    # This document
    ├── ARCHITECTURE.md
    └── API.md
```

### D. Key ECI Resources (for knowledge base)

- ECI Official Site: https://eci.gov.in
- Voter Portal: https://voterportal.eci.gov.in
- cVIGIL App: https://cvigil.eci.gov.in
- National Voters' Service Portal: https://www.nvsp.in
- Voter Helpline: 1950
- ECI Press Releases: https://eci.gov.in/press-release/press-releases/
- MyNeta (candidate affidavits): https://www.myneta.info

---

*Document prepared for Prompt Wars Hackathon — Antigravity × GCP track.*  
*For queries: Navdeep Singh | SRMIST Delhi-NCR Campus*

---
**© 2026 Chunav Saathi — Civic Technology for Democratic India**