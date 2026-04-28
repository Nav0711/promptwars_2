from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ..services.gemini import generate_chat_response

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: Optional[str] = "en"
    location: Optional[Dict[str, float]] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    suggestions: List[str] = []
    guardrail_triggered: bool = False
    latency_ms: int = 0

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        import time
        start_time = time.time()
        
        response_text, sources, triggered = await generate_chat_response(
            message=req.message,
            language=req.language
        )
        
        end_time = time.time()
        latency = int((end_time - start_time) * 1000)
        
        return ChatResponse(
            response=response_text,
            sources=sources,
            suggestions=["Where is my polling booth?", "What is NOTA?"],
            guardrail_triggered=triggered,
            latency_ms=latency
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
