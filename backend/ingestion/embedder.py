"""
embedder.py — Uses Vertex AI text-embedding-004 for document ingestion.
Falls back to google-genai SDK if Vertex AI is unavailable.
"""
import os

GCP_PROJECT  = os.getenv("GCP_PROJECT_ID", "promptwars2-494413")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")


def generate_embedding(text: str) -> list:
    """
    Generates a 768-dimensional embedding using Vertex AI text-embedding-004.
    Used during ingestion (synchronous).
    """
    try:
        import vertexai
        from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput

        vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
        model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        inputs = [TextEmbeddingInput(text=text, task_type="RETRIEVAL_DOCUMENT")]
        result = model.get_embeddings(inputs)
        return result[0].values

    except Exception as e:
        print(f"[embedder] Vertex AI failed, trying google-genai fallback: {e}")
        try:
            from google import genai
            client = genai.Client()
            result = client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e2:
            print(f"[embedder] google-genai fallback also failed: {e2}")
            return [0.0] * 768
