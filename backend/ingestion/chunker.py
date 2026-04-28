import re

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    """
    Splits text into chunks of specified size with overlap.
    """
    words = re.findall(r'\S+', text)
    chunks = []
    
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            
            # Create overlap
            overlap_words = []
            overlap_len = 0
            for w in reversed(current_chunk):
                if overlap_len + len(w) + 1 <= overlap:
                    overlap_words.insert(0, w)
                    overlap_len += len(w) + 1
                else:
                    break
            
            current_chunk = overlap_words
            current_length = overlap_len
            
        current_chunk.append(word)
        current_length += len(word) + 1
        
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
