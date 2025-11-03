def preprocess_ade_json(ade_json):
    chunks = []
    for doc in ade_json.get("documents", []):
        text_lines = []
        for field in doc.get("fields", []):
            name = field.get("name", "")
            value = field.get("value", "")
            if value:
                text_lines.append(f"{name}: {value}")
        text = "\n".join(text_lines)
        chunks.append(text)
    return chunks
