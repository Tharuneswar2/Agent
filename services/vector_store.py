from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
import uuid

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "financial_chunks"

def _init_collection():
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance="Cosine")
        )

_init_collection()


def chunk_store(chunks):
    """
    Store embedded chunks into Qdrant with correct payload keys for LangChain.
    """
    points = []
    for ch in chunks:
        text = ch.get("text") or ch.get("content") or ""
        if not text.strip():
            continue

        metadata = ch.get("extraction", {})
        company = metadata.get("company_name" or metadata.get("CompanyName"))

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=ch["embedding"],
                payload={
                    "page_content": text,       # ✅ Required for LangChain
                    "CompanyName": company,     # For company-based filters
                    "source": metadata.get("source", "ADE"),
                    "chunk_index": metadata.get("chunk_index", 0),
                    "page": metadata.get("page", 0),
                    "type": metadata.get("type", "text")
                },
            )
        )

    if not points:
        print("⚠️ No valid chunks to store in Qdrant.")
        return {"stored": 0}

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Stored {len(points)} chunks in Qdrant.")
    return {"stored": len(points)}
