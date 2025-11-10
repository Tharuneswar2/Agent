
from fastapi import FastAPI
from routers.parse_route import router as parse_router
from routers.query_route import router as query_router
from routers.visual_route import router as visual_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Financial AI Agent Backend")
app.include_router(parse_router)
app.include_router(query_router)
app.include_router(visual_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status":"FastAPI is Running..!"}

@app.get("/health")
def health_check():
    return {"status":"OK"}


@app.post("/load_api_key")
def load_api_key(api_key: str):
    import os
    os.environ["VISION_AGENT_API_KEY"] = api_key
    return {"status": "API key loaded successfully."}