from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import asyncio
from services.ade_parser import (
    Status_landingai_ade_jobs,
    get_landingai_ade_output,
    extract_fields_from_ade_output,
)
from services.preprocessor import preprocess_ade_json
from services.embedder import embed_chunks
from services.vector_store import chunk_store
from services.mongo_store import save_document
import logging
import json
import os

router = APIRouter()
logger = logging.getLogger(__name__)

job_id = "cmhoqvlne00hz7ew79g547y1k"


async def test_parse_document():
    """
    Simulates ADE parsing and ingestion flow for a completed job.
    Loads local ade_output.json → preprocess → embed → store
    """
    try:
        logger.info(f"🧠 Starting ADE test pipeline for job {job_id}")

        # Simulate completed job
        status = {
            "job_id": job_id,
            "status": "completed",
            "output_url": "http://example.com/ade_output.json"
        }

        if status.get("status") != "completed":
            logger.warning(f"⚠️ Job not completed yet: {status}")
            return

        # 1️⃣ Load ADE output (locally for now)
        ade_path = "Reliance_2025_AnnualReport.json"
        if not os.path.exists(ade_path):
            raise FileNotFoundError(f"{ade_path} not found in current directory")

        with open(ade_path, "r") as f:
            ade_output = json.load(f)

        logger.info("📄 ADE output loaded successfully.")
        save_document(ade_output, collection="ade_raw_outputs")

        # 2️⃣ Extract fields using your advanced schema
        extracted_fields = extract_fields_from_ade_output(ade_output)
        save_document(extracted_fields, collection="ade_extracted_fields")
        logger.info("📊 Extracted structured fields saved to MongoDB.")

        # 3️⃣ Preprocess into text chunks
        processed_chunks = preprocess_ade_json(ade_output)
        if not processed_chunks:
            logger.error("❌ No chunks generated during preprocessing.")
            return

        logger.info(f"🧩 Generated {len(processed_chunks)} text chunks.")

        # 4️⃣ Embed chunks
        embedded_chunks = embed_chunks(processed_chunks)
        if not embedded_chunks:
            logger.error("❌ No embeddings generated. Skipping Qdrant upload.")
            return

        logger.info(f"🧠 Embedded {len(embedded_chunks)} chunks successfully.")

        # 5️⃣ Store in Qdrant
        result = chunk_store(embedded_chunks)
        logger.info(f"✅ Stored chunks in Qdrant: {result}")

        # 6️⃣ Mark job as completed
        save_document({"job_id": job_id, "status": "completed"}, collection="ade_jobs")
        print(f"✅ Job {job_id} completed and data loaded successfully.")

    except Exception as e:
        logger.exception(f"❌ Error during ADE pipeline: {str(e)}")
        save_document({"job_id": job_id, "status": "failed", "error": str(e)}, collection="ade_jobs")


if __name__ == "__main__":
    asyncio.run(test_parse_document())
