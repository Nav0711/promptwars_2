from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ..services.gemini import generate_chat_response
from ..services.rate_limiter import ai_rate_limiter

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


# ── Context-aware suggestion chips ───────────────────────────────────────────

_SUGGESTIONS_EN = {
    "booth":       ["Where is my polling booth?", "What time does polling start?", "What ID do I need?"],
    "register":    ["How to update voter details?", "Check my voter registration", "What is Form 6?"],
    "nota":        ["Who gets the seat if NOTA wins?", "How to use NOTA on EVM?", "History of NOTA"],
    "evm":         ["What is VVPAT?", "Is EVM tamper-proof?", "When were EVMs first used?"],
    "mcc":         ["When does MCC come into effect?", "What is banned under MCC?", "How to report MCC violation?"],
    "schedule":    ["When is voting in my state?", "Phase-wise dates for Bihar", "Next election announcement"],
    "default":     ["Where is my polling booth?", "What is NOTA?", "How do I register as a voter?", "What is the Model Code of Conduct?"],
}

_SUGGESTIONS_HI = {
    "booth":       ["मेरा मतदान केंद्र कहाँ है?", "मतदान कितने बजे शुरू होता है?", "कौन से दस्तावेज़ चाहिए?"],
    "register":    ["मतदाता विवरण कैसे अपडेट करें?", "मेरा पंजीकरण जांचें", "फॉर्म 6 क्या है?"],
    "nota":        ["NOTA जीते तो क्या होगा?", "EVM पर NOTA कैसे चुनें?"],
    "default":     ["मेरा मतदान केंद्र कहाँ है?", "NOTA क्या है?", "मतदाता पंजीकरण कैसे करें?"],
}


def _get_suggestions(message: str, language: str) -> List[str]:
    msg = message.lower()
    table = _SUGGESTIONS_HI if language == "hi" else _SUGGESTIONS_EN

    if any(kw in msg for kw in ["booth", "polling", "vote", "केंद्र", "मतदान"]):
        return table.get("booth", table["default"])
    if any(kw in msg for kw in ["register", "registration", "form 6", "पंजीकरण"]):
        return table.get("register", table["default"])
    if any(kw in msg for kw in ["nota", "none of the above"]):
        return table.get("nota", table["default"])
    if any(kw in msg for kw in ["evm", "machine", "electronic"]):
        return table.get("evm", table["default"])
    if any(kw in msg for kw in ["mcc", "code of conduct", "आचार संहिता"]):
        return table.get("mcc", table["default"])
    if any(kw in msg for kw in ["schedule", "date", "phase", "when", "कब", "चरण"]):
        return table.get("schedule", table["default"])

    return table["default"]


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("", response_model=ChatResponse, dependencies=[Depends(ai_rate_limiter)])
async def chat(req: ChatRequest):
    try:
        import time
        start = time.time()

        response_text, sources, triggered = await generate_chat_response(
            message=req.message,
            language=req.language or "en",
        )

        latency = int((time.time() - start) * 1000)
        suggestions = _get_suggestions(req.message, req.language or "en")

        return ChatResponse(
            response=response_text,
            sources=sources,
            suggestions=suggestions,
            guardrail_triggered=triggered,
            latency_ms=latency,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
