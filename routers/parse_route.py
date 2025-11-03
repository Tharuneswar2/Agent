from fastapi import APIRouter, UploadFile,File
import os
import json
from services.ade_parser import call_landingai_ade
from services.preprocessor import preprocess_ade_json
from services.embedder import embed_chunks
from services.vector_store import chunk_store
from services.company_extractor import extract_company_name_from_ade
import re
router = APIRouter()

@router.post("/parse_router")
async def parse_document(file: UploadFile = File(...)):
    """API endpoint to parse a document using LandingAI ADE."""
    try:
        # Read uploaded file
        content = await file.read()

        # Parse with ADE
        result = call_landingai_ade(content, file.filename)
        
        companyName = extract_company_name_from_ade(result)
        
        chunks = preprocess_ade_json(result)

        embeddings = embed_chunks(chunks,companyName)

        chunk_store("financial_docs", embeddings)
        # Save output JSON locally
        os.makedirs("outputs", exist_ok=True)
        output_path = f"outputs/{file.filename}.ade.json"

        # Safely serialize the result
        with open(output_path, "w") as f:
            json.dump(result.model_dump(), f, indent=2)

        return {
            "status": "success",
            "file": file.filename,
            "output_json": output_path,
            # "preview": getattr(result, "markdown", "")[:500]  # show first 500 chars safely
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}
