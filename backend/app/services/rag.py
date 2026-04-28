import json
from .firestore import get_db
from ..ingestion.embedder import generate_embedding

# We'll use Cosine distance for Vector Search
# This assumes the 'rag_chunks' collection has a Vector field named 'embedding'

async def retrieve_context(query: str, top_k: int = 3):
    db = get_db()
    
    query_embedding = generate_embedding(query)
    
    if not db:
        print("Firestore not available. Returning empty context.")
        return [], []
    
    try:
        # GCP Firestore Native Vector Search
        # Requires firestore.Client()
        collection_ref = db.collection('rag_chunks')
        
        # For this prototype, if find_nearest fails, we gracefully return empty.
        from google.cloud.firestore_v1.vector import Vector
        from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
        
        vector_query = collection_ref.find_nearest(
            vector_field="embedding",
            query_vector=Vector(query_embedding),
            distance_measure=DistanceMeasure.COSINE,
            limit=top_k,
        )
        
        docs = vector_query.stream()
        
        contexts = []
        sources = []
        for doc in docs:
            data = doc.to_dict()
            contexts.append(data.get('text', ''))
            sources.append(data.get('source_url', 'Unknown Source'))
            
        return contexts, sources
        
    except Exception as e:
        print(f"Vector search failed: {e}")
        return [], []
