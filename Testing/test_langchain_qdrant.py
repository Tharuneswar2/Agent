# test_langchain_qdrant.py
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient

# 1️⃣ Create embedding model
embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2️⃣ Connect to Qdrant (local or cloud)
qdrant = QdrantClient(url="http://localhost:6333")  # change if using cloud

# 3️⃣ Create vector store
texts = [
    "Revenue increased 20% this quarter",
    "Company profit margin decreased",
    "New market expansion planned"
]

vector_store = Qdrant.from_texts(
    texts=texts,
    embedding=embeddings,
    url="http://localhost:6333",  # or your Qdrant cloud URL
    collection_name="financial_test"
)

# 4️⃣ Query similar text
query = "How is company performance?"
results = vector_store.similarity_search(query, k=2)

print("🔍 Results:")
for doc in results:
    print("-", doc.page_content)
