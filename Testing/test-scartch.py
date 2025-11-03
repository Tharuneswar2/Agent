import json
# Parse the document
with open("agent-finance/outputs/NASDAQ_TSLA_2024.pdf.ade.json", "r") as f:
    data = json.load(f)

# Print the results
print("Extracted Markdown:")
print(data.get("markdown", ""))
print("Extracted Chunks:")
print(data.get("chunks", []))

# Save Markdown to a file
if data.get("markdown"):
    with open('markdown-NASDAQ_TSLA_2024.md', 'w', encoding='utf-8') as f:
        f.write(data.get("markdown", ""))
    print("\nMarkdown content saved to a Markdown file.")
else:
    print("No 'markdown' field found in the response")