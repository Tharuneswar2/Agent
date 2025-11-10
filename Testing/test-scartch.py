from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

records, next_page = client.scroll(
    collection_name="financial_chunks",
    limit=1000  # adjust if needed
)

for r in records:
    client.set_payload(
        collection_name="financial_chunks",
        payload={"CompanyName": "Reliance Industries Limited"},
        points=[r.id]
    )

print("✅ Updated all payloads with CompanyName = 'Reliance Industries Limited'")
