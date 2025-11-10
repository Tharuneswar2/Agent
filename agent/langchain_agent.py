# agent_finance/agent/langchain_agent.py


"""
Financial RAG Agent for Company Data Retrieval
----------------------------------------------
This module connects to Qdrant and MongoDB to answer financial queries
using ADE extraction data and annual report chunks.
"""
import sys
import os
# Local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import os
import re
import logging
from typing import List, Dict
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from services.embedder import get_embedding  
from services.mongo_store import db
from openai import OpenAI 
from services.bedrock_client import BedrockLLM

# Choose your Bedrock model, e.g., 'anthropic.claude-v2' or 'ai21.j2-large'

# -------------------------------
# CONFIGURATION
# -------------------------------

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "financial_chunks")

client = QdrantClient(url=QDRANT_URL)
logger = logging.getLogger(__name__)

# ✅ Initialize OpenAI client (reads OPENAI_API_KEY from env)
llm = OpenAI()
# llm = BedrockLLM(model_id="anthropic.claude-v2")

# -------------------------------
# COMPANY EXTRACTION
# -------------------------------

def extract_company_name(query: str) -> str:
    """
    Extracts company name from query by matching known names in MongoDB.
    Falls back to 'Reliance Industries Limited' if 'reliance' is in query.
    """
    query_lower = query.lower()
    try:
        known_companies = [
            doc["CompanyName"] for doc in db["companies"].find({}, {"CompanyName": 1})
        ]
        for name in known_companies:
            if name.lower() in query_lower:
                return name
    except Exception as e:
        logger.warning(f"MongoDB company lookup failed: {e}")

    if "reliance" in query_lower:
        return "Reliance Industries Limited"
    return "Unknown"

# -------------------------------
# QDRANT RETRIEVAL
# -------------------------------

def get_company_docs(company_name: str, query: str, limit: int = 5) -> List[Dict]:
    """
    Retrieve top relevant chunks from Qdrant for the given company and query.
    """
    try:
        query_vector = get_embedding(query)

        # ✅ Use updated `query_points` API (not `query_vector`)
        search_results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="CompanyName",
                        match=models.MatchValue(value=company_name)
                    )
                ]
            ),
        )

        docs = []
        for r in search_results.points:
            payload = r.payload or {}
            docs.append({
                "text": payload.get("page_content") or payload.get("text", ""),
                "score": r.score,
                "type": payload.get("type", "unknown"),
                "source": payload.get("source", "unknown"),
                "page": payload.get("page", 0),
            })
        return docs

    except Exception as e:
        logger.error(f"Qdrant retrieval error: {e}")
        return []

# -------------------------------
# LLM SYNTHESIS
# -------------------------------

# def synthesize_answer(query: str, docs: List[Dict]) -> str:
#     if not docs:
#         return "I couldn’t find any relevant information for your query."

#     context = "\n\n".join([f"[{d['type']}] {d['text']}" for d in docs])

#     prompt = f"""
#         You are a financial analysis assistant.
#         Use the following context from company documents (ADE extraction + Annual Reports)
#         to answer the user query truthfully and concisely.

#         User Query: {query}

#         Context:
#         {context}

#         If the answer cannot be determined from the context, say so clearly.
#         Provide numbers and years exactly as in the context.
#         """ 

#     try:
#         # return llm.generate(prompt=prompt, temperature=0.2, max_tokens=512)
#         # openai response
#         response = llm.generate(prompt=prompt, temperature=0.2, max_tokens=512)
#     except Exception as e:
#         logger.error(f"Bedrock LLM error: {e}")
#         return "Error generating response."


def synthesize_answer(query: str, docs: List[Dict]) -> str:
    """
    Synthesizes an answer using retrieved document chunks and OpenAI GPT model.
    """
    if not docs:
        return "I couldn’t find any relevant information for your query."

    context = "\n\n".join([f"[{d['type']}] {d['text']}" for d in docs])

    prompt = f"""
You are a financial analysis assistant.
Use the following context from company documents (ADE extraction + Annual Reports)
to answer the user query truthfully and concisely.

User Query: {query}

Context:
{context}

If the answer cannot be determined from the context, say so clearly.
Provide numbers and years exactly as in the context.
"""

    try:
        # ✅ Use new OpenAI v1 SDK syntax
        response = llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful financial RAG assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"LLM synthesis error: {e}")
        return "Error generating response."


# -------------------------------
# MAIN PIPELINE
# -------------------------------

def answer_financial_query(query: str) -> Dict:
    """
    Full pipeline:
    1️⃣ Identify company
    2️⃣ Retrieve top chunks
    3️⃣ Generate LLM answer
    """
    company = extract_company_name(query)
    docs = get_company_docs(company, query)
    answer = synthesize_answer(query, docs)

    return {
        "query": query,
        "company": company,
        "answer": answer,
        "sources": docs,
    }

# -------------------------------
# Example usage
# -------------------------------

if __name__ == "__main__":
    q = "What is the total revenue of Reliance Industries in FY 2025?"
    response = answer_financial_query(q)

    print("\n🧾 Answer:", response["answer"])
    print("\n📊 Company:", response["company"])
    print("\n📚 Sources:", [d["source"] for d in response["sources"]])
