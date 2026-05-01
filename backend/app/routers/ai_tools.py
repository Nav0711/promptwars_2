"""
ai_tools.py — Advanced AI endpoints for Chunav Saathi.

Routes:
  GET  /v1/ai/quiz          — Gemini-powered voter awareness quiz
  POST /v1/ai/explain       — Election jargon explainer
  POST /v1/ai/summarize_eci — Summarize an ECI notification URL
"""
import json
import re
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

from ..services.vertex_service import generate_vertex_response
from ..services.rag import retrieve_context
from ..services.rate_limiter import ai_rate_limiter

router = APIRouter(prefix="/ai", tags=["ai-tools"])


# ── Models ─────────────────────────────────────────────────────────────────────

class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer: int  # 0-indexed
    explanation: str
    difficulty: str = "medium"

class QuizResponse(BaseModel):
    title: str
    title_hi: str
    questions: List[QuizQuestion]
    total_questions: int

class ExplainRequest(BaseModel):
    term: str
    language: Optional[str] = "en"

class ExplainResponse(BaseModel):
    term: str
    simple_explanation: str
    example: str
    source_url: Optional[str] = None

class SummarizeRequest(BaseModel):
    content: str
    language: Optional[str] = "en"

class SummarizeResponse(BaseModel):
    summary: str
    key_points: List[str]
    category: str


# ── Quiz Endpoint ──────────────────────────────────────────────────────────────

QUIZ_PROMPT_EN = """
You are an educational quiz generator for Indian elections.

Generate EXACTLY 5 multiple choice questions based on the knowledge below.
Mix of easy, medium and hard difficulty.

Respond with ONLY a raw JSON object — no markdown, no code fences, no explanation.
Structure:
{{
  "title": "India Election Awareness Quiz",
  "title_hi": "भारत चुनाव जागरूकता प्रश्नोत्तरी",
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0,
      "explanation": "...",
      "difficulty": "easy"
    }}
  ],
  "total_questions": 5
}}

KNOWLEDGE BASE:
{context}
"""

QUIZ_PROMPT_HI = """
आप भारतीय चुनावों पर एक शैक्षिक प्रश्नोत्तरी जनरेटर हैं।
नीचे दिए गए ज्ञान के आधार पर EXACTLY 5 बहुविकल्पीय प्रश्न बनाएं।
केवल raw JSON object दें — कोई markdown नहीं।
Structure:
{{
  "title": "India Election Awareness Quiz",
  "title_hi": "भारत चुनाव जागरूकता प्रश्नोत्तरी",
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0,
      "explanation": "...",
      "difficulty": "easy"
    }}
  ],
  "total_questions": 5
}}

KNOWLEDGE BASE:
{context}
"""

@router.get("/quiz", response_model=QuizResponse, dependencies=[Depends(ai_rate_limiter)])
async def get_voter_quiz(language: str = "en"):
    """
    Generates a fresh 5-question voter awareness quiz using Gemini 1.5 Flash.
    Grounded in the RAG knowledge base for factual accuracy.
    """
    # Pull varied context from the knowledge base
    contexts, _ = await retrieve_context(
        "election voting rules NOTA EVM registration polling booth MCC",
        top_k=5
    )
    context_str = "\n\n---\n\n".join(contexts) if contexts else _fallback_context()

    prompt_template = QUIZ_PROMPT_HI if language == "hi" else QUIZ_PROMPT_EN
    prompt = prompt_template.format(context=context_str)

    response_text, is_error = await generate_vertex_response(
        message=prompt,
        context="You output ONLY raw valid JSON. No markdown. No extra text.",
        language=language,
    )

    if is_error:
        return _static_quiz(language)

    try:
        # Strip any markdown code fences that might slip through
        cleaned = response_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        quiz_data = json.loads(cleaned)
        return quiz_data
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[ai_tools] Quiz JSON parse error: {e}\nRaw: {response_text[:300]}")
        return _static_quiz(language)


# ── Explainer Endpoint ─────────────────────────────────────────────────────────

EXPLAIN_PROMPT = """
Explain the Indian election term "{term}" in very simple language.
Respond ONLY as raw JSON:
{{
  "term": "{term}",
  "simple_explanation": "One or two plain sentences a first-time voter can understand.",
  "example": "A real-world example of how this works.",
  "source_url": "Official ECI or government URL if applicable, else null"
}}
"""

@router.post("/explain", response_model=ExplainResponse, dependencies=[Depends(ai_rate_limiter)])
async def explain_election_term(req: ExplainRequest):
    """
    Breaks down complex election jargon into simple language using Gemini.
    """
    prompt = EXPLAIN_PROMPT.format(term=req.term)

    # First check if RAG has context on this term
    contexts, _ = await retrieve_context(req.term, top_k=2)
    context_str = "\n".join(contexts) if contexts else ""

    response_text, is_error = await generate_vertex_response(
        message=prompt,
        context=f"You output ONLY raw valid JSON.\n\nKNOWLEDGE: {context_str}",
        language=req.language or "en",
    )

    if is_error:
        raise HTTPException(status_code=500, detail="AI explainer failed")

    try:
        cleaned = response_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return json.loads(cleaned)
    except Exception as e:
        print(f"[ai_tools] Explain parse error: {e}")
        return {
            "term": req.term,
            "simple_explanation": f"{req.term} is an important part of the Indian election process.",
            "example": "Please refer to eci.gov.in for detailed information.",
            "source_url": "https://eci.gov.in",
        }


# ── ECI Content Summarizer ─────────────────────────────────────────────────────

SUMMARIZE_PROMPT = """
You are a civic journalist summarizing an official Indian Election Commission document.

Summarize the following content for a general public reader.
Respond ONLY as raw JSON:
{{
  "summary": "2-3 sentence summary.",
  "key_points": ["point 1", "point 2", "point 3"],
  "category": "one of: Schedule | MCC | Candidate | Results | Notices | General"
}}

CONTENT:
{content}
"""

@router.post("/summarize", response_model=SummarizeResponse, dependencies=[Depends(ai_rate_limiter)])
async def summarize_eci_content(req: SummarizeRequest):
    """
    Summarizes any ECI press release or notification content using Gemini.
    """
    prompt = SUMMARIZE_PROMPT.format(content=req.content[:3000])  # cap tokens

    response_text, is_error = await generate_vertex_response(
        message=prompt,
        context="You output ONLY raw valid JSON. Be concise and factual.",
        language=req.language or "en",
    )

    if is_error:
        raise HTTPException(status_code=500, detail="AI summarizer failed")

    try:
        cleaned = response_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return json.loads(cleaned)
    except Exception as e:
        print(f"[ai_tools] Summarize parse error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response")


# ── Helpers ────────────────────────────────────────────────────────────────────

def _fallback_context() -> str:
    return """
    Indian elections are governed by the Representation of the People Act, 1951.
    The minimum voting age is 18. NOTA (None of the Above) allows voters to reject all candidates.
    EVMs are used since 2004. Model Code of Conduct applies from election announcement date.
    Voter ID (EPIC card) or 12 alternative IDs are accepted at the polling booth.
    Polling booths are open from 7 AM to 6 PM on election day.
    """

def _static_quiz(language: str) -> dict:
    if language == "hi":
        return {
            "title": "India Election Awareness Quiz",
            "title_hi": "भारत चुनाव जागरूकता प्रश्नोत्तरी",
            "total_questions": 5,
            "questions": [
                {"id": 1, "question": "भारत में मतदान की न्यूनतम आयु क्या है?", "options": ["16 वर्ष", "18 वर्ष", "21 वर्ष", "25 वर्ष"], "correct_answer": 1, "explanation": "भारत के संविधान के 61वें संशोधन (1989) द्वारा मतदान की आयु 21 से घटाकर 18 वर्ष की गई।", "difficulty": "easy"},
                {"id": 2, "question": "NOTA का पूरा नाम क्या है?", "options": ["None Of The Allowed", "None Of The Above", "No Other Than Authorized", "National Option To Abstain"], "correct_answer": 1, "explanation": "NOTA का मतलब है None Of The Above। यह 2013 में सुप्रीम कोर्ट के आदेश पर लागू किया गया था।", "difficulty": "easy"},
                {"id": 3, "question": "मतदाता सूची में नाम जोड़ने के लिए कौन सा फॉर्म भरना होता है?", "options": ["Form 7", "Form 8", "Form 6", "Form 4"], "correct_answer": 2, "explanation": "Form 6 नए मतदाताओं के पंजीकरण के लिए है। Form 7 नाम हटाने के लिए और Form 8 सुधार के लिए है।", "difficulty": "medium"},
                {"id": 4, "question": "आदर्श आचार संहिता (MCC) कब लागू होती है?", "options": ["मतदान के दिन", "चुनाव की घोषणा की तारीख से", "मतदान से एक सप्ताह पहले", "नामांकन की अंतिम तिथि से"], "correct_answer": 1, "explanation": "आदर्श आचार संहिता चुनाव कार्यक्रम की घोषणा की तारीख से लागू होती है और परिणाम घोषणा तक जारी रहती है।", "difficulty": "medium"},
                {"id": 5, "question": "EVM का पूरा नाम क्या है?", "options": ["Electronic Voter Machine", "Electronic Voting Machine", "Electoral Vote Monitor", "Election Verification Module"], "correct_answer": 1, "explanation": "EVM का मतलब है Electronic Voting Machine। इसका उपयोग भारत में 2004 के आम चुनाव से सभी निर्वाचन क्षेत्रों में किया जा रहा है।", "difficulty": "easy"},
            ],
        }
    return {
        "title": "India Election Awareness Quiz",
        "title_hi": "भारत चुनाव जागरूकता प्रश्नोत्तरी",
        "total_questions": 5,
        "questions": [
            {"id": 1, "question": "What is the minimum voting age in India?", "options": ["16 years", "18 years", "21 years", "25 years"], "correct_answer": 1, "explanation": "The 61st Constitutional Amendment (1989) lowered the voting age from 21 to 18 years.", "difficulty": "easy"},
            {"id": 2, "question": "What does NOTA stand for?", "options": ["None Of The Allowed", "None Of The Above", "No Other Than Authorized", "National Option To Abstain"], "correct_answer": 1, "explanation": "NOTA stands for None Of The Above. It was introduced in 2013 following a Supreme Court ruling.", "difficulty": "easy"},
            {"id": 3, "question": "Which form is used to register as a new voter?", "options": ["Form 7", "Form 8", "Form 6", "Form 4"], "correct_answer": 2, "explanation": "Form 6 is for new voter registration. Form 7 is for deletion and Form 8 is for corrections.", "difficulty": "medium"},
            {"id": 4, "question": "When does the Model Code of Conduct (MCC) come into effect?", "options": ["On polling day", "From the date of election announcement", "One week before polling", "From the last date of nomination"], "correct_answer": 1, "explanation": "The MCC comes into effect from the date of announcement of election schedule and remains until results.", "difficulty": "medium"},
            {"id": 5, "question": "How long are polling booths open on election day?", "options": ["6 AM – 4 PM", "7 AM – 6 PM", "8 AM – 5 PM", "9 AM – 7 PM"], "correct_answer": 1, "explanation": "Polling booths typically open at 7 AM and close at 6 PM, though hours may vary by state and constituency.", "difficulty": "easy"},
        ],
    }
