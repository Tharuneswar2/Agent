import json
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from langchain_huggingface import HuggingFaceEmbeddings
import re 
# === CONFIG ===
QDRANT_URL = "http://localhost:6333"
COLLECTION = "financial_docs"
ADE_JSON_PATH = "outputs/NASDAQ_TSLA_2024.pdf.ade.json"

# === INIT ===
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
client = QdrantClient(url=QDRANT_URL)

# Recreate collection for clean indexing
if COLLECTION in [c.name for c in client.get_collections().collections]:
    client.delete_collection(COLLECTION)

client.create_collection(
    COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

def extract_company_name_from_ade(ade_json: dict) -> str | None:
    """
    Dynamically extract the company name from ADE JSON output.
    Works well for SEC filings, regardless of company.
    """
    try:
        chunks = ade_json.get("chunks", [])
        candidate_names = []

        for c in chunks:
            text = c.get("text", "").strip()

            # Skip small fragments or generic lines
            if not text or len(text) < 3 or len(text.split()) > 6:
                continue

            # Look for strong company-like patterns
            if re.search(r"\b(Inc\.?|Incorporated|Corporation|Corp\.?|Ltd\.?|LLC|PLC|Company)\b", text, re.IGNORECASE):
                candidate_names.append(text)

        # Pick the most confident candidate (shortest valid one)
        if candidate_names:
            candidate_names.sort(key=len)
            return candidate_names[0].strip()

        # Fallback: look for uppercase block text near top of doc
        all_text = " ".join([c.get("text", "") for c in chunks[:20]])
        match = re.search(
            r"\b([A-Z][A-Z0-9,\.\-& ]{2,100}?(?:INC\.?|CORP\.?|LTD\.?|LLC|COMPANY|CORPORATION|LIMITED))\b",
            all_text,
        )
        if match:
            return match.group(1).strip().title()

    except Exception as e:
        print("⚠️ Error extracting company name:", e)

    return None

# === LOAD ADE JSON ===
with open(ADE_JSON_PATH, "r") as f:
    ade_data = json.load(f)

chunks = ade_data.get("chunks", [])
companyName = extract_company_name_from_ade(ade_data)

points = []
for chunk in chunks:
    text = chunk.get("text") or chunk.get("markdown") or ""
    if not text.strip():
        continue  # skip empty chunks

    vector = embeddings.embed_query(text)
    point_id = str(uuid.uuid4())
    metadata = {
        "chunk_id": chunk.get("chunk_id") or point_id,
        "chunk_type": chunk.get("chunk_type", "text"),
        "CompanyName":companyName,
        "page": chunk.get("grounding", [{}])[0].get("page", None),
    }

    points.append(PointStruct(id=point_id, vector=vector, payload={
        "page_content": text,
        "metadata": metadata
    }))

if points:
    client.upsert(collection_name=COLLECTION, points=points)
    print(f"✅ Indexed {len(points)} chunks into '{COLLECTION}' collection.")
else:
    print("⚠️ No valid chunks found to index.")
