
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI  # ✅ modern import

load_dotenv()

# =======================
# 1️⃣  Connect to Qdrant
# =======================
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
print(f"🔗 Connecting to Qdrant at: {QDRANT_URL}")

client = QdrantClient(url=QDRANT_URL, prefer_grpc=False)

# =======================
# 2️⃣  Create Embeddings
# =======================
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# =======================
# 3️⃣  Setup VectorStore + Retriever
# =======================
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="financial_docs",
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 8})  # top 8 chunks

# =======================
# 4️⃣  Initialize LLM (OpenAI)
# =======================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# =======================
# 5️⃣  Define Query + Retrieve
# =======================
query = "Summarize Tesla’s 2024 debt and equity ratios and compare them to 2023."
# query = "who is the Chief Financial Officer ?"
# query = "who is the CEO of Tesla ?"
print(f"\n🧠 Running retrieval for query: {query}\n")

docs = retriever.invoke(query)  # ✅ modern call
print(f"✅ Retrieved {len(docs)} relevant chunks from Qdrant.\n")

print("🔍 Retrieved Chunks:\n")
for doc in docs:
    print(f"---\n{doc.page_content[:500]}\n")  # print first 500 chars per chunk

# =======================
# 6️⃣  Build Enhanced Financial Prompt
# =======================
context = "\n\n".join(d.page_content for d in docs)

prompt = f"""
You are a financial analysis assistant.

Use the context below (from Tesla's 2024 financial filing) to answer the question.
If numeric values for total debt, total equity, or ratios appear, compute the debt-to-equity ratio.
Otherwise, respond factually based on what is available.

Context:
{context}

Question:
{query}

Provide a concise and factual financial summary.
"""

# =======================
# 7️⃣  Generate Answer
# =======================
print("\n🤖 Thinking...\n")
response = llm.invoke(prompt)

print("=== 💬 AI Response ===")
print(response.content if hasattr(response, "content") else response)
