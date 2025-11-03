from langchain_huggingface import HuggingFaceEmbeddings
import uuid
from qdrant_client.models import PointStruct
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(chunks,companyName):
    points = []
    for chunk in chunks:
        text = chunk.get("text") or chunk.get("markdown") or ""
        vector = embeddings.embed_query(text)
        point_id = str(uuid.uuid4())
        metadata = {
            "chunk_id": chunk.get("chunk_id") or point_id,
            "chunk_type": chunk.get("chunk_type", "text"),
            "CompanyName":companyName,
            "page": chunk.get("grounding", [{}])[0].get("page", None),
        }
        points.append(PointStruct(id=point_id,vector=vector,payload={
            "page_content": text,
            "metadata": metadata
        }))
    return points