
# #agent/langchain_agent.py
# import os
# from dotenv import load_dotenv
# from langchain_qdrant import Qdrant
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableLambda
# from qdrant_client import QdrantClient
# from langchain_community.chat_models import ChatOpenAI
# import sys, os
# from services.company_extractor import extract_company_name_from_ade

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from agent.tools.calc_tool import compute_ratios
# load_dotenv()

# def make_agent():
#     """Create a retriever + LLM QA agent."""

#     # ✅ Initialize Qdrant client
#     qdrant_client = QdrantClient(
#         url=os.getenv("QDRANT_URL", "http://localhost:6333"),
#         prefer_grpc=False
#     )

#     # ✅ Embeddings model
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#     # ✅ Connect Qdrant + embeddings
#     vectorstore = Qdrant(
#         client=qdrant_client,
#         collection_name="financial_docs",
#         embeddings=embeddings
#     )

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

#     # ✅ OpenAI model (use .env for security)
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         openai_api_key=os.getenv("OPENAI_API_KEY")
#     )

#     # ✅ Prompt
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are a financial analysis assistant. Use the provided context below to answer accurately and concisely. "
#                    "If the answer is not found in the context, say 'The context does not contain that information.'"),
#         ("human", "{input}")
#     ])
    
#     def chain_func(inputs):
#         query = inputs["input"]
#         docs = retriever.invoke(query)
#         # print(f"Retrieved {len(docs)} documents for the query.")
#         # print(f"\n\n\n Documents: {docs}")
#         context = "\n\n".join([d.page_content for d in docs])

#         # Try extracting numeric values automatically
#         if "ratio" in query.lower():
#             context += "\n\nFinancial Calculation Context:\n" + compute_ratios({"text": context})

#         formatted_prompt = prompt.format_messages(input=f"Context:\n{context}\n\nQuestion: {query}")
#         response = llm.invoke(formatted_prompt)
#         return {"answer": str(response), "sources": [d.metadata for d in docs]}


#     return RunnableLambda(chain_func)


# def run_query(agent, query: str):
#     """Run query safely through the agent."""
#     if isinstance(query, dict):
#         query = query.get("query") or query.get("text") or query.get("question") or str(query)
#     elif not isinstance(query, str):
#         query = str(query)

#     result = agent.invoke({"input": query})
#     return result




# if __name__ == "__main__":
#     qa = make_agent()
#     response = run_query(qa, "Who is the Chief Financial Officer")
#     print(response)

# # # agent/langchain_agent.py
# # import os
# # import re
# # import sys
# # from dotenv import load_dotenv
# # from qdrant_client import QdrantClient
# # from qdrant_client.http import models as rest
# # from langchain_qdrant import Qdrant
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain_core.runnables import RunnableLambda
# # from langchain_community.chat_models import ChatOpenAI

# # # Add project root to path
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# # from agent.tools.calc_tool import compute_ratios

# # load_dotenv()


# # def extract_company_name(query: str) -> str | None:
# #     """Extract company name dynamically from queries like 'Who is the CFO of Tesla?'"""
# #     match = re.search(r"of\s+([A-Z][A-Za-z0-9& ]+)", query)
# #     return match.group(1).strip() if match else None


# # def make_agent():
# #     """Create a retriever + LLM QA agent with company-aware context."""

# #     # ✅ Qdrant setup
# #     qdrant_client = QdrantClient(
# #         url=os.getenv("QDRANT_URL", "http://localhost:6333"),
# #         prefer_grpc=False
# #     )

# #     # ✅ Embeddings
# #     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# #     # ✅ Vector store
# #     vectorstore = Qdrant(
# #         client=qdrant_client,
# #         collection_name="financial_docs",
# #         embeddings=embeddings
# #     )

# #     llm = ChatOpenAI(
# #         model="gpt-4o-mini",
# #         openai_api_key=os.getenv("OPENAI_API_KEY")
# #     )

# #     # ✅ Base prompt
# #     prompt = ChatPromptTemplate.from_messages([
# #         ("system",
# #          "You are a financial analysis assistant. Use the provided context below to answer accurately and concisely. "
# #          "If the answer is not found in the context, say 'The context does not contain that information.'"),
# #         ("human", "{input}")
# #     ])

# #     def chain_func(inputs):
# #         query = inputs["input"]
# #         company = extract_company_name(query)
# #         q_filter = None

# #         # ✅ Apply company-level filtering if company detected
# #         if company:
# #             q_filter = rest.Filter(
# #                 must=[rest.FieldCondition(
# #                     key="company",
# #                     match=rest.MatchValue(value=company)
# #                 )]
# #             )
# #             print(f"🔍 Detected company: {company}")
# #         else:
# #             print("⚠️ No company detected — performing global search.")

# #         # ✅ Perform retrieval
# #         docs = vectorstore.similarity_search(query, k=10, filter=q_filter)
# #         context = "\n\n".join([d.page_content for d in docs]) or "No context retrieved."

# #         # ✅ Auto financial ratio computation if needed
# #         if "ratio" in query.lower():
# #             context += "\n\nFinancial Calculation Context:\n" + compute_ratios({"text": context})

# #         formatted_prompt = prompt.format_messages(input=f"Context:\n{context}\n\nQuestion: {query}")
# #         response = llm.invoke(formatted_prompt)

# #         return {
# #             "answer": str(response),
# #             "company": company or "N/A",
# #             "sources": [d.metadata for d in docs]
# #         }

# #     return RunnableLambda(chain_func)


# # def run_query(agent, query: str):
# #     """Safely run a query through the financial QA agent."""
# #     if isinstance(query, dict):
# #         query = query.get("query") or query.get("text") or query.get("question") or str(query)
# #     elif not isinstance(query, str):
# #         query = str(query)

# #     return agent.invoke({"input": query})


# # if __name__ == "__main__":
# #     qa = make_agent()
# #     print(run_query(qa, "Who is the Chief Financial Officer of Tesla"))



# import os
# import re
# import sys
# from dotenv import load_dotenv
# from qdrant_client import QdrantClient
# from qdrant_client import models as rest
# from langchain_qdrant import Qdrant
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableLambda
# from langchain_community.chat_models import ChatOpenAI

# # Local imports
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from agent.tools.calc_tool import compute_ratios
# from services.company_extractor import extract_company_name_from_ade  # For future ADE integration

# # ==============================
# # Load environment variables
# # ==============================
# load_dotenv()


# # ==========================================================
# # 1️⃣  Extract company name from user query (robust & flexible)
# # ==========================================================
# def extract_company_name(query: str) -> str | None:
#     """
#     Extracts company name dynamically from queries like:
#     'Who is the CFO of Tesla?', 'Debt ratio for Apple Inc', etc.
#     """
#     match = re.search(r"\b(?:of|for)\s+([A-Z][A-Za-z0-9&., ]+)", query, re.IGNORECASE)
#     if match:
#         # Normalize: remove commas and periods, uppercase
#         return match.group(1).strip().replace(",", "").upper()
#     return None


# # ==========================================================
# # 2️⃣  Build a flexible Qdrant filter for company matching
# # ==========================================================
# # def build_company_filter(company: str):
# #     normalized_company = re.sub(r"[^A-Za-z0-9 ]", "", company).strip().upper()

# #     return rest.Filter(
# #         must=[
# #             rest.FieldCondition(
# #                 key="CompanyName",
# #                 match=rest.MatchText(text=normalized_company)
# #             )
# #         ]
# #     )

# def build_company_filter(company: str):
#     normalized = re.sub(r"[^A-Za-z0-9 ]", "", company).strip().upper()
#     return rest.Filter(
#         must=[
#             rest.FieldCondition(
#                 key="CompanyName",
#                 match=rest.MatchText(text=normalized)
#             )
#         ]
#     )


# # ==========================================================
# # 3️⃣  Retrieve documents (company-aware + fallback)
# # ==========================================================
# def get_company_docs(vectorstore, company, query):
#     company_filter = build_company_filter(company)

#     # Try with filter first
#     docs = vectorstore.similarity_search(query, k=10, filter=company_filter)

#     if not docs:
#         print("⚠️ Filtered search empty — retrying with global search.")
#         # Clean query by removing company name for better semantic matching
#         cleaned_query = re.sub(r"\b" + re.escape(company) + r"\b", "", query, flags=re.IGNORECASE)
#         docs = vectorstore.similarity_search(cleaned_query.strip(), k=10)

#     print(f"✅ Retrieved {len(docs)} documents for {company}")
#     for d in docs:
#         print("📄 Metadata:", d.metadata)

#     return docs


# # ==========================================================
# # 4️⃣  Main Agent Builder
# # ==========================================================
# def make_agent():
#     """Create a retriever + LLM QA agent with dynamic company context."""

#     # ✅ Connect to Qdrant
#     qdrant_client = QdrantClient(
#         url=os.getenv("QDRANT_URL", "http://localhost:6333"),
#         prefer_grpc=False
#     )

#     # ✅ Setup Embeddings
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#     # ✅ Vectorstore
#     vectorstore = Qdrant(
#         client=qdrant_client,
#         collection_name="financial_docs",
#         embeddings=embeddings
#     )

#     # ✅ LLM
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         openai_api_key=os.getenv("OPENAI_API_KEY")
#     )

#     # ✅ Prompt Template
#     prompt = ChatPromptTemplate.from_messages([
#         ("system",
#          "You are a financial analysis assistant. Use the provided context below to answer accurately and concisely. "
#          "If the answer is not found in the context, say 'The context does not contain that information.'"),
#         ("human", "{input}")
#     ])

#     # ==========================================================
#     # 5️⃣  Chain Function (Dynamic, Smart Retrieval)
#     # ==========================================================
#     def chain_func(inputs):
#         query = inputs["input"]
#         company = extract_company_name(query)

#         # Contextual expansion for CFO/CEO queries
#         if "cfo" in query.lower():
#             query += " Chief Financial Officer finance management leadership executive officer"
#         elif "ceo" in query.lower():
#             query += " Chief Executive Officer company leadership management"

#         # Company-specific retrieval
#         if company:
#             print(f"🏢 Detected company: {company}")
#             docs = get_company_docs(vectorstore, company, query)
#         else:
#             print("⚠️ No company detected — performing global search.")
#             docs = vectorstore.similarity_search(query, k=10)

#         # Build context
#         context = "\n\n".join([d.page_content for d in docs]) or "No context retrieved."

#         # Auto financial ratio computation
#         if "ratio" in query.lower():
#             context += "\n\nFinancial Calculation Context:\n" + compute_ratios({"text": context})

#         # Prompt assembly
#         formatted_prompt = prompt.format_messages(input=f"Context:\n{context}\n\nQuestion: {query}")
#         response = llm.invoke(formatted_prompt)

#         return {
#             "answer": str(response),
#             "company": company or "N/A",
#             "sources": [d.metadata for d in docs]
#         }

#     return RunnableLambda(chain_func)


# # ==========================================================
# # 6️⃣  Query Runner (safe)
# # ==========================================================
# def run_query(agent, query: str):
#     """Safely run a query through the financial QA agent."""
#     if isinstance(query, dict):
#         query = query.get("query") or query.get("text") or query.get("question") or str(query)
#     elif not isinstance(query, str):
#         query = str(query)

#     return agent.invoke({"input": query})


# # ==========================================================
# # 7️⃣  Standalone Debug Runner
# # ==========================================================
# if __name__ == "__main__":
#     qa = make_agent()
#     print(run_query(qa, "Who is the Chief Financial Officer of Tesla"))





import os
import re
import sys
from dotenv import load_dotenv

# Qdrant imports
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from qdrant_client.http import exceptions as qdrant_exceptions

# LangChain imports
from langchain_qdrant import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.chat_models import ChatOpenAI

# Local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent.tools.calc_tool import compute_ratios
from services.company_extractor import extract_company_name_from_ade  # For future ADE integration


# Local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent.tools.calc_tool import compute_ratios
from services.company_extractor import extract_company_name_from_ade  # For future ADE integration

# ==============================
# Load environment variables
# ==============================
load_dotenv()


# ==========================================================
# 1️⃣  Extract company name from user query (robust & flexible)
# ==========================================================
def extract_company_name(query: str) -> str | None:
    """
    Extracts company name dynamically from queries like:
    'Who is the CFO of Tesla?', 'Debt ratio for Apple Inc', etc.
    """
    match = re.search(r"\b(?:of|for)\s+([A-Z][A-Za-z0-9&., ]+)", query, re.IGNORECASE)
    if match:
        # Normalize: remove commas and periods, uppercase
        return match.group(1).strip().replace(",", "").upper()
    return None


# ==========================================================
# 2️⃣  Build a flexible Qdrant filter for company matching
# ==========================================================
# def build_company_filter(company: str):
#     normalized_company = re.sub(r"[^A-Za-z0-9 ]", "", company).strip().upper()

#     return rest.Filter(
#         must=[
#             rest.FieldCondition(
#                 key="CompanyName",
#                 match=rest.MatchText(text=normalized_company)
#             )
#         ]
#     )

# def build_company_filter(company: str):
#     normalized = re.sub(r"[^A-Za-z0-9 ]", "", company).strip().upper()
#     return rest.Filter(
#         must=[
#             rest.FieldCondition(
#                 key="CompanyName",
#                 match=rest.MatchText(text=normalized)
#             )
#         ]
#     )

def normalize_company(name: str):
    """Normalize company names (case-insensitive, remove suffixes and punctuation)."""
    name = name.upper()
    name = re.sub(r"[,.\-&]", " ", name)
    for suffix in ["INC", "LTD", "LLC", "CORP", "CO", "COMPANY", "PLC", "LIMITED"]:
        name = re.sub(rf"\b{suffix}\b", "", name)
    return re.sub(r"\s+", " ", name).strip()

def resolve_company_name_semantic(company: str, embedder, qdrant_client: QdrantClient, collection: str):
    """
    Try to find the most semantically similar company name
    using embeddings from your vectorstore.
    """
    try:
        embedding = embedder.embed_query(company)
        search_results = qdrant_client.search(
            collection_name=collection,
            query_vector=embedding,
            limit=1,
            with_payload=True
        )
        if search_results:
            best_match = search_results[0].payload.get("CompanyName", company)
            score = search_results[0].score
            if score > 0.6:  # Adjust threshold based on dataset
                print(f"🔍 Semantic match found: {best_match} (score={score:.2f})")
                return best_match
    except Exception as e:
        print(f"⚠️ Semantic search fallback: {e}")
    return company

def build_company_filter(company: str, embedder=None, qdrant_client=None, company_collection="financial_docs"):
    """
    Build the most robust possible Qdrant filter:
    1. Normalize the name.
    2. Try semantic company resolution (if embedder + Qdrant available).
    3. Try fuzzy filter (if Qdrant supports it).
    4. Fallback to normalized exact match.
    """
    normalized = normalize_company(company)

    # Step 1: Try semantic matching if embedder is provided
    if embedder and qdrant_client:
        resolved_name = resolve_company_name_semantic(normalized, embedder, qdrant_client, company_collection)
    else:
        resolved_name = normalized

    # Step 2: Try fuzzy text match (for Qdrant ≥ 1.9)
    try:
        print(f"🔠 Using fuzzy filter for: {resolved_name}")
        return rest.Filter(
            must=[
                rest.FieldCondition(
                    key="CompanyName",
                    match=rest.MatchText(text=resolved_name, fuzzy=True)
                )
            ]
        )
    except (TypeError, qdrant_exceptions.UnexpectedResponse, Exception):
        # Step 3: Fallback exact normalized filter
        print("⚠️ Fuzzy not supported — using normalized exact match instead.")
        return rest.Filter(
            must=[
                rest.FieldCondition(
                    key="CompanyName",
                    match=rest.MatchText(text=resolved_name)
                )
            ]
        )
from langchain_community.embeddings import OpenAIEmbeddings

qdrant_client = QdrantClient(url="http://localhost:6333")
# embedder = OpenAIEmbeddings(model="text-embedding-3-small")
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ==========================================================
# 3️⃣  Retrieve documents (company-aware + fallback)
# ==========================================================
def get_company_docs(vectorstore, company, query):
    company_filter = build_company_filter(
        company="Tesla",
        embedder=embedder,
        qdrant_client=qdrant_client,
        company_collection="financial_docs"
    )
    # Try with filter first
    docs = vectorstore.similarity_search(query, k=10, filter=company_filter)

    if not docs:
        print("⚠️ Filtered search empty — retrying with global search.")
        # Clean query by removing company name for better semantic matching
        cleaned_query = re.sub(r"\b" + re.escape(company) + r"\b", "", query, flags=re.IGNORECASE)
        docs = vectorstore.similarity_search(cleaned_query.strip(), k=10)

    print(f"✅ Retrieved {len(docs)} documents for {company}")
    for d in docs:
        print("📄 Metadata:", d.metadata)

    return docs


# ==========================================================
# 4️⃣  Main Agent Builder
# ==========================================================
def make_agent():
    """Create a retriever + LLM QA agent with dynamic company context."""

    # ✅ Connect to Qdrant
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        prefer_grpc=False
    )

    # ✅ Setup Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # ✅ Vectorstore
    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name="financial_docs",
        embeddings=embeddings
    )

    # ✅ LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # ✅ Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a financial analysis assistant. Use the provided context below to answer accurately and concisely. "
         "If the answer is not found in the context, say 'The context does not contain that information.'"),
        ("human", "{input}")
    ])

    # ==========================================================
    # 5️⃣  Chain Function (Dynamic, Smart Retrieval)
    # ==========================================================
    def chain_func(inputs):
        query = inputs["input"]
        company = extract_company_name(query)

        # Contextual expansion for CFO/CEO queries
        if "cfo" in query.lower():
            query += " Chief Financial Officer finance management leadership executive officer"
        elif "ceo" in query.lower():
            query += " Chief Executive Officer company leadership management"

        # Company-specific retrieval
        if company:
            print(f"🏢 Detected company: {company}")
            docs = get_company_docs(vectorstore, company, query)
        else:
            print("⚠️ No company detected — performing global search.")
            docs = vectorstore.similarity_search(query, k=10)

        # Build context
        context = "\n\n".join([d.page_content for d in docs]) or "No context retrieved."

        # Auto financial ratio computation
        if "ratio" in query.lower():
            context += "\n\nFinancial Calculation Context:\n" + compute_ratios({"text": context})

        # Prompt assembly
        formatted_prompt = prompt.format_messages(input=f"Context:\n{context}\n\nQuestion: {query}")
        response = llm.invoke(formatted_prompt)

        return {
            "answer": str(response),
            "company": company or "N/A",
            "sources": [d.metadata for d in docs]
        }

    return RunnableLambda(chain_func)


# ==========================================================
# 6️⃣  Query Runner (safe)
# ==========================================================
def run_query(agent, query: str):
    """Safely run a query through the financial QA agent."""
    if isinstance(query, dict):
        query = query.get("query") or query.get("text") or query.get("question") or str(query)
    elif not isinstance(query, str):
        query = str(query)

    return agent.invoke({"input": query})


# ==========================================================
# 7️⃣  Standalone Debug Runner
# ==========================================================
if __name__ == "__main__":
    qa = make_agent()
    print(run_query(qa, "Who is the Chief Financial Officer of Tesla"))