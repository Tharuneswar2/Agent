from langchain_agent import extract_company_name, get_company_docs, vectorstore

q = "What is net profit of Reliance Industries for FY 2025?"
company = extract_company_name(q)
print("Extracted company:", company)

docs = get_company_docs(company, q)
print("Docs returned:", len(docs))
if docs:
    print("Top doc metadata:", docs[0].metadata)
    print("Top doc snippet:", docs[0].page_content[:300])
