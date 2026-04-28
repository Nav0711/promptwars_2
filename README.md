# 🗳️ Chunav Saathi — India Election Intelligence Hub

> **Prompt Wars Hackathon Submission**
> Built with Antigravity, GCP (Firestore, Cloud Run, Vertex AI), Next.js, and FastAPI.

Chunav Saathi is an AI-powered election intelligence platform built for Indian citizens. It combines a real-time election dashboard with a rigorously guardrailed, RAG-powered conversational assistant to answer questions about the Indian electoral process.

## Features
- **AI Chatbot**: Powered by Gemini Flash, heavily guardrailed against political bias, grounded in a RAG knowledge base.
- **Interactive Dashboard**: Track active elections, upcoming phases, and live stats.
- **Booth Finder**: Locate polling booths easily.
- **Knowledge Base**: Searchable FAQs built from official ECI guidelines.
- **Multilingual Support**: Switch seamlessly between English and Hindi.

## Tech Stack
- **Frontend**: Next.js 14 (App Router), Tailwind CSS, shadcn/ui.
- **Backend**: FastAPI (Python), Uvicorn.
- **AI/ML**: Google GenAI (Gemini 2.5 Flash), Vertex AI Embeddings (`text-embedding-004`).
- **Data**: Google Cloud Firestore (Native Vector Search).

## Local Development & Setup

Prerequisites: Docker and Docker Compose.

1. **Clone the repository**
2. **Environment Variables**: Provide a valid `GEMINI_API_KEY` to test the AI.
3. **Run with Docker Compose**:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   docker-compose up --build
   ```
4. Access the platform:
   - Frontend: `http://localhost:3000`
   - Backend API Docs: `http://localhost:8000/docs`

## Guardrails & Safety
Chunav Saathi employs a multi-layered safety strategy:
- **Pre-query Classifier**: Regex-based blocks for prediction or opinion-seeking prompts.
- **RAG Injection**: Context fetched dynamically via Cosine distance search is strictly supplied to the LLM to prevent hallucinations.
- **System Prompts**: Mandates political neutrality and source citation.

## Authors
Created for the **Prompt Wars — Powered by Antigravity × GCP** hackathon.
