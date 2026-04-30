"""
rag.py — RAG context retrieval using Firestore Vector Search.
Uses Vertex AI text-embedding-004 for query embedding.
"""
from .firestore import get_db

async def retrieve_context(query: str, top_k: int = 3):
    """
    Embeds the query using Vertex AI, then performs ANN search
    against the 'rag_chunks' Firestore collection.
    Returns: (contexts: list[str], sources: list[str])
    """
    db = get_db()

    # Generate embedding asynchronously via Vertex AI
    try:
        from .vertex_service import embed_text_async
        query_embedding = await embed_text_async(query)
    except Exception as e:
        print(f"[rag] embedding failed, using mock: {e}")
        query_embedding = [0.0] * 768

    if not db:
        print("[rag] Firestore not available. Returning empty context.")
        return [], []

    try:
        from google.cloud.firestore_v1.vector import Vector
        from google.cloud.firestore_v1.base_vector_query import DistanceMeasure

        collection_ref = db.collection("rag_chunks")
        vector_query = collection_ref.find_nearest(
            vector_field="embedding",
            query_vector=Vector(query_embedding),
            distance_measure=DistanceMeasure.COSINE,
            limit=top_k,
        )

        contexts = []
        sources  = []
        for doc in vector_query.stream():
            data = doc.to_dict()
            text = data.get("text", "").strip()
            source = data.get("source_url", "ECI Official Document")
            if text:
                contexts.append(text)
                sources.append(source)

        return contexts, sources

    except Exception as e:
        print(f"[rag] Vector search failed: {e}")
        return [], []
