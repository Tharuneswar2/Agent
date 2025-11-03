import os
from agentic_doc.parse import parse

# Set environment variables (use .env in production for security)
os.environ["VISION_AGENT_API_KEY"] = "OHE2eTI2MGsxcWh3eGoxbWU1NjNvOjE3Rjd6UlFPazgwUE03VGRlYldMQU40TUFXeEVtU2o5"
os.environ["LANDINGAI_ENDPOINT_HOST"] = "https://api.va.landing.ai" 

def call_landingai_ade(file_bytes: bytes, filename: str):
    """Handles calling LandingAI ADE and returning parsed result."""
    temp_path = f"/tmp/{filename}"

    # Save uploaded file temporarily
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    results = parse(
        temp_path,
        include_marginalia=True,               
        include_metadata_in_markdown=True    
    )
    if not results:
        raise ValueError("No result returned from ADE parser.")

    return results[0]
