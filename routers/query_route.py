from fastapi import APIRouter 
from agent.langchain_agent import make_agent , run_query
from agent.tools import calc_tool
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query:str
    
qa_agent = make_agent()

router = APIRouter()

@router.post("/query_router")
async def query_agent(request:QueryRequest):
    query = request.query
    
    result = run_query(qa_agent,query=query)
    
    return{
        "status":"success",
        "query":query,
        "response":result.get('answer'),
    }    