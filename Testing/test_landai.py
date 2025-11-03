from agentic_doc.parse import parse

results = parse(
    "samples/sample_10k.pdf",
    include_marginalia=False,  # Exclude marginalia from output
    include_metadata_in_markdown=False  # Exclude metadata from markdown
)

print("Number of results:", len(results))