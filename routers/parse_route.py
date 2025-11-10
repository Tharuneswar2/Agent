# agent_finance/routers/parse_route.py

from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import asyncio
import json
import logging

from services.ade_parser import (
    call_landingai_ade_jobs,
    Status_landingai_ade_jobs,
    get_landingai_ade_output,
    extract_fields_from_ade_output,
)
from services.preprocessor import preprocess_ade_json
from services.embedder import embed_chunks
from services.vector_store import chunk_store
from services.mongo_store import save_document

router = APIRouter()
logger = logging.getLogger(__name__)


# ✅ Background worker for ADE → extract → embed → store
async def process_ade_job(job_id: str, report_file: UploadFile = None):
    delay = 5
    try:
        while True:
            status = Status_landingai_ade_jobs(job_id)
            job_state = status.get("status")

            if job_state == "completed":
                output_url = status.get("output_url")
                ade_output = get_landingai_ade_output(output_url)
                save_document(ade_output, collection="ade_raw_outputs")

                extracted_fields = extract_fields_from_ade_output(ade_output)
                save_document(extracted_fields, collection="ade_extracted_fields")

                processed_chunks = preprocess_ade_json(ade_output)
                embedded_ade_chunks = embed_chunks(processed_chunks)
                chunk_store(embedded_ade_chunks)

                print(f"✅ ADE job {job_id} parsed & stored successfully.")

                # Optional: also handle report_file if provided
                if report_file:
                    await process_report_file(report_file, ade_output)

                save_document({"job_id": job_id, "status": "completed"}, collection="ade_jobs")
                break

            elif job_state in ["processing", "running"]:
                await asyncio.sleep(delay)
                delay = min(delay + 3, 30)
            else:
                save_document({"job_id": job_id, "status": "failed"}, collection="ade_jobs")
                print(f"❌ Job {job_id} failed: {status}")
                break

    except Exception as e:
        save_document({"job_id": job_id, "status": "error", "error": str(e)}, collection="ade_jobs")
        print(f"⚠️ Error in background ADE job {job_id}: {e}")


# ✅ Helper: Process and store Annual Report file
async def process_report_file(report_file: UploadFile, ade_output: dict = None):
    try:
        report_data = json.loads((await report_file.read()).decode("utf-8"))
        company_name = ade_output.get("extraction", {}).get("company_name", "Unknown") if ade_output else "Unknown"
        save_document(report_data, collection="annual_reports")

        report_chunks = []
        for idx, ch in enumerate(report_data.get("chunks", [])):
            text = ch.get("markdown", "")
            if not text.strip():
                continue
            report_chunks.append({
                "text": text,
                "metadata": {
                    "CompanyName": company_name,
                    "page": ch.get("grounding", {}).get("page", 0),
                    "type": ch.get("type", "text"),
                    "chunk_index": idx,
                    "source": report_data.get("metadata", {}).get("filename", report_file.filename),
                },
            })

        embedded_report = embed_chunks(report_chunks)
        chunk_store(embedded_report)
        print(f"✅ Stored {len(embedded_report)} report chunks for {company_name}")

    except Exception as e:
        print(f"⚠️ Error storing report file: {e}")


# ✅ Unified endpoint: parse ADE → auto-store ADE & Report
@router.post("/parse_router")
async def parse_and_store_documents(
    background_tasks: BackgroundTasks,
    ade_file: UploadFile = File(...),
    report_file: UploadFile = File(None)
):
    """
    Unified endpoint:
    1️⃣ Submits ADE extraction job to LandingAI
    2️⃣ Tracks completion asynchronously
    3️⃣ On completion → saves ADE output + embeddings
    4️⃣ Optionally embeds & stores the annual report file
    """
    # Read ADE input content
    content = await ade_file.read()
    filename = ade_file.filename

    # Step 1️⃣ — Create ADE Job
    ade_response = call_landingai_ade_jobs(content, filename)
    job_id = ade_response.get("job_id")

    if not job_id:
        raise ValueError(f"ADE job creation failed: {ade_response}")

    # Step 2️⃣ — Run ADE + optional report processing in background
    background_tasks.add_task(process_ade_job, job_id, report_file)

    # Step 3️⃣ — Return job info immediately
    return {
        "status": "started",
        "job_id": job_id,
        "message": "ADE job submitted successfully. It will automatically process and store ADE + report data when complete.",
    }


@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Check ADE job processing status."""
    from services.mongo_store import db
    job = db["ade_jobs"].find_one({"job_id": job_id})
    if not job:
        return {"job_id": job_id, "status": "unknown"}
    return {"job_id": job_id, "status": job.get("status", "unknown")}
