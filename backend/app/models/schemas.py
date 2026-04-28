from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str = "en"
    location: Optional[Dict[str, float]] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    suggestions: List[str] = []
    guardrail_triggered: bool = False
    latency_ms: int = 0

class PhaseInfo(BaseModel):
    phase: int
    date: str
    constituencies: int
    status: str

class ElectionInfo(BaseModel):
    state: str
    type: str
    phases: List[PhaseInfo]

class ActiveElectionsResponse(BaseModel):
    elections: List[ElectionInfo]

class DashboardStats(BaseModel):
    active_elections: int
    days_until_next_phase: int
    total_seats: int
    eligible_voters_millions: float
