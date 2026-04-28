from google import genai
import os

def generate_embedding(text: str):
    """
    Generates a 768-dimensional vector embedding for a given text
    using Google's text-embedding-004 model.
    """
    client = genai.Client()
    try:
        # Note: the PRD specifies text-embedding-004
        result = client.models.embed_content(
            model='text-embedding-004',
            contents=text
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return mock 768-d vector for dev if API fails
        return [0.0] * 768
