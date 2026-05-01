from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, elections, chat, ai_tools

app = FastAPI(
    title="Chunav Saathi API",
    version="2.1.0",
    description="India Election Intelligence Platform powered by Vertex AI & Firestore",
)

# CORS — allow all for hackathon, tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/v1")
app.include_router(elections.router, prefix="/v1")
app.include_router(chat.router,      prefix="/v1")
app.include_router(ai_tools.router,  prefix="/v1")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "2.1.0",
        "ai_backend": "vertex_ai_gemini_1_5_flash",
        "project": "promptwars2-494413",
    }

@app.get("/")
def root():
    return {"message": "Welcome to Chunav Saathi API v2.1 — India Election Intelligence"}
