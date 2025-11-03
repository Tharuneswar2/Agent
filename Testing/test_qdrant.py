from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import numpy as np

# Step 1: Set up Qdrant client
qdrant_client = QdrantClient(url="http://localhost:6333")  # Replace with your Qdrant instance URL

# Step 2: Initialize the embeddings model (Sentence-Transformers example)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use any sentence-transformer model

# Step 3: Define a function to create embeddings for your query
def get_query_embedding(query: str):
    return embedding_model.encode(query).tolist()

# Step 4: Define a function to search Qdrant for relevant documents
def search_documents(query: str, collection_name: str = "financial_docs", top_k: int = 10):
    # Get the query embedding
    query_embedding = get_query_embedding(query)
    
    # Perform search in Qdrant
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k,  # Adjust based on how many results you want
        with_payload=True
    )
    
    return search_result

# Step 5: Query your Qdrant collection
query = "financial summary for December 31, 2024"
results = search_documents(query)

# Step 6: Print the retrieved results
print(f"Query: {query}\n")
for idx, result in enumerate(results):
    print(f"--- Document {idx + 1} ---")
    print(f"ID: {result.id}")
    print(result.payload.get("text"))  # Change to the appropriate field, depending on your data schema
    print("\n")
