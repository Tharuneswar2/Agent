from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams ,Distance
load_dotenv()
client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
def chunk_store(collection_name: str, points):
    if collection_name in [c.name for c in client.get_collections().collections]:
        client.upsert(collection_name=collection_name, points=points)
        return
    
    client.create_collection(
        collection_name,
        vectors_config=VectorParams(size=384,distance=Distance.COSINE),
    )
    
    client.upsert(collection_name=collection_name, points=points)
    