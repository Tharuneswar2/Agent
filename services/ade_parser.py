import os
import requests
import json
import logging
# Set environment variables (use .env in production for security)
# os.environ["VISION_AGENT_API_KEY"] = "OHE2eTI2MGsxcWh3eGoxbWU1NjNvOjE3Rjd6UlFPazgwUE03VGRlYldMQU40TUFXeEVtU2o5"
os.environ["VISION_AGENT_API_KEY"] = "aTkybjAyNHQybW04ZmwyNHpsa212Ok1ndTdzdXZKWUNvMFBBSzlGQmc2OE50YkpmdlBvYzJZ"
os.environ["LANDINGAI_ENDPOINT_HOST"] = "https://api.va.landing.ai/v1/ade/parse/jobs"
os.environ["LANDINGAI_JOB_STATUS"] = "https://api.va.landing.ai/v1/ade/parse/jobs/"
os.environ["LANDINGAI_FIELDS_EXTRACT"] = "https://api.va.landing.ai/v1/ade/extract"

logging.basicConfig(level=logging.INFO)

def call_landingai_ade_jobs(file_bytes: bytes, filename: str):
    """Handles calling LandingAI ADE and returning parsed result."""
    logging.info("Calling LandingAI ADE API.")
    print(f"Calling LandingAI ADE API.")
    temp_path = f"/tmp/{filename}"

    # Save uploaded file temporarily
    with open(temp_path, "wb") as f:
        f.write(file_bytes)
        
    # Call LandingAI ADE API
    headers = {
        "Authorization": f"Bearer {os.environ['VISION_AGENT_API_KEY']}"
    }
    files = {
        "document": open(temp_path, "rb")
    }
    url = os.environ["LANDINGAI_ENDPOINT_HOST"]
    response = requests.post(
        url,
        headers=headers,
        files=files,
        data={"model": "dpt-2-latest"}
    )

    # if response.status_code != 200:
    #     raise ValueError("Failed to call LandingAI ADE API.")
    logging.info(f"LandingAI ADE job response: {response.json()}")
    print(f"LandingAI ADE job response: {response.json()}")
    return response.json()

def Status_landingai_ade_jobs(job_id: str):
    """Check the status of a LandingAI ADE job."""
    headers = {
        "Authorization": f"Bearer {os.environ['VISION_AGENT_API_KEY']}"
    }
    response = requests.get(f"{os.environ['LANDINGAI_JOB_STATUS']}{job_id}", headers=headers)

    if response.status_code != 200:
        raise ValueError("Failed to check LandingAI ADE job status.")
    logging.info(f"LandingAI ADE job status response: {response.json()}")
    print(f"LandingAI ADE job status response: {response.json()}")
    return response.json()

def get_landingai_ade_output(output_url: str):
    """Fetch the output JSON from LandingAI ADE using the provided URL."""
    response = requests.get(output_url)

    if response.status_code != 200:
        raise ValueError("Failed to fetch LandingAI ADE output.")
    logging.info(f"LandingAI ADE output fetched successfully.")
    print(f"LandingAI ADE output fetched successfully.")
    return response.json()

def load_schema():
    with open('schema_content.json', 'r') as f:
        schema_content = f.read()
    return schema_content

def extract_fields_from_ade_output(ade_output: dict):
    logging.info("Extracting fields from ADE output using schema.")
    schema_content = load_schema()
    # create a tmp file to store the ade_output
    temp_path = "/tmp/ade_output.json"
    with open(temp_path, "w") as f:
        json.dump(ade_output.get('markdown'), f)
    logging.info(f"Temporary ADE output saved to {temp_path}.")
    print(f"Temporary ADE output saved to {temp_path}.")
    files = {'markdown': open(temp_path, 'rb')}
    response = requests.post(
        os.environ["LANDINGAI_FIELDS_EXTRACT"],
        headers={
            "Authorization": f"Bearer {os.environ['VISION_AGENT_API_KEY']}"
        },
        files=files,
        data = {'schema': schema_content, 'model': 'extract-latest'}
    )
    return response.json()