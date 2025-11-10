from fastapi import APIRouter 
from agent.langchain_agent import answer_financial_query
from agent.tools import calc_tool
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query:str
    
router = APIRouter()
@router.get("/health_query")
async def health_check():
    return {"status":"Query Router is Healthy"}

@router.post("/query_router")
async def query_agent(request:QueryRequest):
    query = request.query
    
    result = answer_financial_query(query)
    print("Query Result:", result)
    return{
        "status":"success",
        "query":query,
        "response":result.get('answer'),
    }    

