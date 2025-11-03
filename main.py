
from fastapi import FastAPI
from routers.parse_route import router as parse_router
from routers.query_route import router as query_router

app = FastAPI(title="Financial AI Agent Backend")
app.include_router(parse_router)
app.include_router(query_router)


@app.get("/")
def root():
    return {"status":"FastAPI is Running..!"}

@app.get("/health")
def health_check():
    return {"status":"OK"}
