"""
vertex_service.py
Vertex AI integration for Chunav Saathi.
Uses Application Default Credentials (ADC) in production (Cloud Run)
and GEMINI_API_KEY for local development.
"""
import os
import asyncio
from typing import Optional

import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    SafetySetting,
    HarmCategory,
    HarmBlockThreshold,
    Content,
    Part,
)
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput

# ── Config ────────────────────────────────────────────────────────────────────
GCP_PROJECT    = os.getenv("GCP_PROJECT_ID", "promptwars2-494413")
GCP_LOCATION   = os.getenv("GCP_LOCATION",   "us-central1")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL",   "gemini-1.5-flash-002")
EMBED_MODEL    = "text-embedding-004"

# Safety config — strict on hate speech / harassment
_SAFETY_SETTINGS = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
]

_GENERATION_CONFIG = GenerationConfig(
    temperature=0.2,
    max_output_tokens=1024,
    top_p=0.8,
)

# Lazy init — only initialised once per process
_vertex_ready = False

def _init_vertex():
    global _vertex_ready
    if not _vertex_ready:
        vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
        _vertex_ready = True

# ── Embedding ─────────────────────────────────────────────────────────────────

def embed_text(text: str, task_type: str = "RETRIEVAL_QUERY") -> list[float]:
    """
    Returns a 768-dimensional vector for the given text using
    Vertex AI text-embedding-004 (best-in-class multilingual support).
    """
    _init_vertex()
    try:
        model = TextEmbeddingModel.from_pretrained(EMBED_MODEL)
        inputs = [TextEmbeddingInput(text=text, task_type=task_type)]
        result = model.get_embeddings(inputs)
        return result[0].values
    except Exception as e:
        print(f"[vertex_service] embed_text error: {e}")
        return [0.0] * 768

async def embed_text_async(text: str, task_type: str = "RETRIEVAL_QUERY") -> list[float]:
    """Async wrapper for embed_text (runs in thread pool)."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, embed_text, text, task_type)

# ── Chat / Generation ─────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Chunav Saathi (चुनाव साथी), a neutral Indian election information assistant.

Your ONLY job is to provide factual, unbiased information about Indian elections.

Rules you MUST follow:
1. NEVER express opinions on political parties, candidates, or governments.
2. NEVER predict election outcomes or interpret exit polls.
3. ALWAYS respond in the same language the user wrote in (Hindi or English).
4. ALWAYS cite your source based on the knowledge base context provided below.
5. If unsure, say: "I recommend checking eci.gov.in directly."
6. If asked for political opinions, decline politely and redirect to factual info.

KNOWLEDGE BASE CONTEXT:
{context}

USER LANGUAGE: {language}
CURRENT DATE: {current_date}
"""

async def generate_vertex_response(
    message: str,
    context: str = "No additional context available.",
    language: str = "en",
    current_date: str = "",
) -> tuple[str, bool]:
    """
    Generates a chat response using Vertex AI Gemini 1.5 Flash.
    Returns (response_text, is_error).
    """
    import datetime
    if not current_date:
        current_date = datetime.date.today().isoformat()

    _init_vertex()

    system_instruction = SYSTEM_PROMPT.format(
        context=context,
        language="Hindi" if language == "hi" else "English",
        current_date=current_date,
    )

    try:
        model = GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=system_instruction,
            safety_settings=_SAFETY_SETTINGS,
            generation_config=_GENERATION_CONFIG,
        )

        # Run in thread pool to keep FastAPI async
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model.generate_content(message)
        )
        return response.text, False

    except Exception as e:
        print(f"[vertex_service] generate error: {e}")
        return "मुझे खेद है, मैं अभी उत्तर देने में असमर्थ हूँ। / I'm sorry, I'm unable to answer right now.", True
