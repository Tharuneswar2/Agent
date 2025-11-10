from sentence_transformers import SentenceTransformer

# Initialize once
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    """
    Takes a list of chunks and generates embeddings for their text.
    Returns the same chunks with embedding vectors added.
    """
    texts = [ch["text"] for ch in chunks]
    embeddings = _model.encode(texts, convert_to_tensor=False).tolist()

    for i, emb in enumerate(embeddings):
        chunks[i]["embedding"] = emb

    return chunks
def get_embedding(text):
    """
    Generate embedding for a single text string.
    """
    embedding = _model.encode(text, convert_to_tensor=False).tolist()
    return embedding