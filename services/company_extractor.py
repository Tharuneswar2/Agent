import re
def extract_company_name_from_ade(ade_json: dict) -> str | None:
    """
    Dynamically extract the company name from ADE JSON output.
    Works well for SEC filings, regardless of company.
    """
    try:
        chunks = ade_json.get("chunks", [])
        candidate_names = []

        for c in chunks:
            text = c.get("text", "").strip()

            # Skip small fragments or generic lines
            if not text or len(text) < 3 or len(text.split()) > 6:
                continue

            # Look for strong company-like patterns
            if re.search(r"\b(Inc\.?|Incorporated|Corporation|Corp\.?|Ltd\.?|LLC|PLC|Company)\b", text, re.IGNORECASE):
                candidate_names.append(text)

        # Pick the most confident candidate (shortest valid one)
        if candidate_names:
            candidate_names.sort(key=len)
            return candidate_names[0].strip()

        # Fallback: look for uppercase block text near top of doc
        all_text = " ".join([c.get("text", "") for c in chunks[:20]])
        match = re.search(
            r"\b([A-Z][A-Z0-9,\.\-& ]{2,100}?(?:INC\.?|CORP\.?|LTD\.?|LLC|COMPANY|CORPORATION|LIMITED))\b",
            all_text,
        )
        if match:
            return match.group(1).strip().title()

    except Exception as e:
        print("⚠️ Error extracting company name:", e)

    return None

