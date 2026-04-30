"""
gemini.py — Orchestrates the full RAG + chat pipeline.
Now uses Vertex AI as the primary engine with a fallback to google-genai SDK.
"""
import os
from .guardrails import check_input_guardrails, get_guardrail_message
from .rag import retrieve_context

# Determine which backend to use
USE_VERTEX = os.getenv("USE_VERTEX_AI", "true").lower() == "true"

async def generate_chat_response(message: str, language: str = "en"):
    """
    Full RAG + generation pipeline.
    Returns: (response_text, sources, guardrail_triggered)
    """
    # 1. Pre-query guardrail check
    if check_input_guardrails(message):
        return get_guardrail_message(message, language), [], True

    # 2. Retrieve context via RAG (Firestore Vector Search)
    contexts, sources = await retrieve_context(message)
    context_str = "\n\n---\n\n".join(contexts) if contexts else "No specific documents found. Use your general knowledge about Indian elections."

    # 3. Generate response
    if USE_VERTEX:
        from .vertex_service import generate_vertex_response
        response_text, is_error = await generate_vertex_response(
            message=message,
            context=context_str,
            language=language,
        )
        if is_error:
            # Fallback to google-genai SDK
            response_text = await _fallback_genai_response(message, context_str, language)
    else:
        response_text = await _fallback_genai_response(message, context_str, language)

    return response_text, list(set(sources)), False


async def _fallback_genai_response(message: str, context: str, language: str) -> str:
    """Fallback using google-genai SDK (uses GEMINI_API_KEY env var)."""
    try:
        from google import genai
        from google.genai import types

        SYSTEM_INSTRUCTION = f"""You are Chunav Saathi, a neutral Indian election information assistant.
Never express opinions on political parties or candidates.
Never predict election outcomes.
Respond in {'Hindi' if language == 'hi' else 'English'}.
CONTEXT: {context}
"""
        client = genai.Client()
        response = await client.aio.models.generate_content(
            model='gemini-2.0-flash',
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=1024,
            )
        )
        return response.text
    except Exception as e:
        print(f"[gemini fallback] error: {e}")
        return "I'm sorry, I am unable to answer right now. Please try again later."
