from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, elections, chat

app = FastAPI(title="Chunav Saathi API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/v1")
app.include_router(elections.router, prefix="/v1")
app.include_router(chat.router, prefix="/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
