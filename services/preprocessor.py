# import re

# def preprocess_ade_json(ade_output: dict):
#     """
#     Preprocess ADE JSON into structured chunks suitable for RAG ingestion.
#     - Extracts markdown & text.
#     - Creates chunk objects with metadata (page number, section type, etc.)
#     """
#     chunks = []
#     markdown_text = ade_output.get("markdown", "")

#     # Clean markdown text
#     markdown_text = re.sub(r"<::.*?::>", "", markdown_text)
#     markdown_text = re.sub(r"\n{2,}", "\n", markdown_text.strip())

#     # Each item in ADE's "chunks" can have its own markdown
#     for i, ch in enumerate(ade_output.get("chunks", [])):
#         text = ch.get("markdown", "").strip()
#         if not text:
#             continue

#         chunk = {
#             "id": f"ade_chunk_{i}",
#             "text": text,
#             "page": ch.get("grounding", {}).get("page", 0),
#             "type": ch.get("type", "unknown"),
#             "metadata": {
#                 "source": "ADE",
#                 "chunk_index": i,
#                 "page": ch.get("grounding", {}).get("page", 0),
#                 "type": ch.get("type", "unknown")
#             }
#         }
#         chunks.append(chunk)

#     # If chunks are empty, use the top-level markdown as fallback
#     if not chunks and markdown_text:
#         chunks = [{"id": "ade_markdown_full", "text": markdown_text, "metadata": {"source": "ADE"}}]

#     return chunks
import re
from tqdm import tqdm

def clean_text(text: str) -> str:
    """Clean text from unwanted spaces, artifacts, or HTML."""
    text = re.sub(r"<[^>]+>", " ", text)  # remove HTML tags
    text = re.sub(r"\s+", " ", text).strip()
    return text


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def preprocess_ade_json(ade_json):
    """
    Extract text from ADE output JSON and split into small chunks for embedding.
    Expected ADE structure: { "pages": [ {"text": "..."} ] } or list of dicts.
    """
    all_texts = []

    # Handle both dict and list formats
    if isinstance(ade_json, dict):
        if "pages" in ade_json:
            for page in ade_json["pages"]:
                if isinstance(page, dict) and "text" in page:
                    cleaned = clean_text(page["text"])
                    if cleaned:
                        all_texts.append(cleaned)
        elif "data" in ade_json:
            # Fallback: ADE sometimes returns "data": [{"page_content": "..."}]
            for item in ade_json["data"]:
                text = item.get("text") or item.get("page_content")
                if text:
                    cleaned = clean_text(text)
                    all_texts.append(cleaned)
        else:
            # last resort: flatten entire dict values
            for v in ade_json.values():
                if isinstance(v, str):
                    all_texts.append(clean_text(v))

    elif isinstance(ade_json, list):
        for item in ade_json:
            if isinstance(item, dict):
                text = item.get("text") or item.get("page_content")
                if text:
                    all_texts.append(clean_text(text))

    # Create chunks
    all_chunks = []
    for text in tqdm(all_texts, desc="Batches"):
        for chunk in chunk_text(text):
            all_chunks.append({"text": chunk, "metadata": {"source": "ADE"}})

    return all_chunks
