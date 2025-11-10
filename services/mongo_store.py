from pymongo import MongoClient
import os
from datetime import datetime
import re

# =====================================================
# MongoDB Setup
# =====================================================
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "agent_finance_db")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# =====================================================
# Utility Functions
# =====================================================
def normalize_company_name(name: str) -> str:
    """Normalize company name for consistent indexing."""
    name = name.upper()
    name = re.sub(r"[,.\-&]", " ", name)
    for suffix in ["INC", "LTD", "LLC", "CORP", "CO", "COMPANY", "PLC", "LIMITED"]:
        name = re.sub(rf"\b{suffix}\b", "", name)
    return re.sub(r"\s+", " ", name).strip()


# =====================================================
# Document Save Functions
# =====================================================
def save_document(document: dict, collection: str = "documents"):
    """Generic save for any ADE or RAG document."""
    collection_ref = db[collection]
    if not document:
        return {"status": "error", "message": "Empty document data"}
    document["created_at"] = datetime.utcnow()
    collection_ref.insert_one(document)
    return {"status": "success", "collection": collection}



def save_schema_document(schema_data: dict):
    """
    Save structured ADE schema-extracted financial data.
    Expected structure matches your JSON schema (company_name, fiscal_year, etc.)
    """
    if not schema_data or "company_name" not in schema_data:
        return {"status": "error", "message": "Missing company_name in schema_data"}

    company = normalize_company_name(schema_data["company_name"])
    collection = db["financial_schemas"]

    schema_data["_company_key"] = company
    schema_data["created_at"] = datetime.utcnow()

    existing = collection.find_one({"_company_key": company})
    if existing:
        collection.update_one({"_company_key": company}, {"$set": schema_data})
        msg = "updated"
    else:
        collection.insert_one(schema_data)
        msg = "inserted"

    return {"status": msg, "company": company}


def save_text_chunks(chunks: list, company: str):
    """
    Save RAG text chunks (from Markdown / embeddings preprocessing).
    """
    company_key = normalize_company_name(company)
    collection = db["document_chunks"]

    if not chunks:
        return {"status": "error", "message": "No chunks to save"}

    records = []
    for c in chunks:
        records.append({
            "_company_key": company_key,
            "CompanyName": company,
            "text": c.get("text") or c.get("content") or str(c),
            "metadata": c.get("metadata", {}),
            "created_at": datetime.utcnow()
        })

    if records:
        collection.insert_many(records)

    return {"status": "success", "count": len(records)}


# =====================================================
# Retrieval Functions
# =====================================================
def get_documents_by_company(company: str, mode: str = "chunks"):
    """
    Retrieve company-specific data from Mongo.
    mode="chunks" → text-based RAG context
    mode="schema" → ADE structured schema data
    """
    company_key = normalize_company_name(company)

    if mode == "schema":
        record = db["financial_schemas"].find_one({"_company_key": company_key})
        return record or {}

    elif mode == "chunks":
        docs = list(db["document_chunks"].find({"_company_key": company_key}))
        return docs

    else:
        return []


def get_all_companies():
    """List all company names stored in schemas."""
    return [d["_company_key"] for d in db["financial_schemas"].find({}, {"_company_key": 1})]
