from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Connect to Qdrant
qdrant = Qdrant(
    url="http://localhost:6333",
    collection_name="financial_docs",
    embeddings=embeddings,
)

# Suppose parsed_docs is a list of text chunks from your parsed PDF
texts = [d["content"] for d in parsed_docs]  # adjust to your structure

# Add to Qdrant
qdrant.add_texts(texts)
print("✅ Parsed document chunks stored in Qdrant!")
