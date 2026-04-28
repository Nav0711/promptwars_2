import os
from google import genai
from google.genai import types
from .guardrails import check_input_guardrails, get_guardrail_message
from .rag import retrieve_context

# Initialize client. Requires GEMINI_API_KEY env var
client = genai.Client()

SYSTEM_INSTRUCTION_TEMPLATE = """
You are Chunav Saathi, a neutral Indian election information assistant.
You must:
1. Never express opinions on political parties, candidates, or governments.
2. Never predict election outcomes.
3. Answer factually about the election process.
4. Always cite your source based on the context provided.
5. Respond in the same language as the user.

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER LANGUAGE: {language}
"""

async def generate_chat_response(message: str, language: str = "en"):
    # 1. Pre-query guardrail check
    if check_input_guardrails(message):
        return get_guardrail_message(message), [], True

    # 2. Retrieve Context via RAG
    contexts, sources = await retrieve_context(message)
    context_str = "\n\n".join(contexts) if contexts else "No additional context available."

    # 3. Format System Instruction
    system_instruction = SYSTEM_INSTRUCTION_TEMPLATE.format(
        context=context_str,
        language=language
    )

    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
            )
        )
        # 4. Return response with actual sources
        return response.text, list(set(sources)), False
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return "I'm sorry, I am unable to answer right now.", [], False
