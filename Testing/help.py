# from qdrant_client import QdrantClient
# from qdrant_client.http import models

# # Connect to your Qdrant instance
# client = QdrantClient(url="http://localhost:6333")

# # Define the chunk_id you want to find
# target_chunk_id = "19e24fca-1689-4e20-a446-b6628c9e9a02"

# # Query Qdrant with a filter
# results = client.scroll(
#     collection_name="financial_docs",
#     scroll_filter=models.Filter(
#         must=[
#             models.FieldCondition(
#                 key="metadata.chunk_id",
#                 match=models.MatchValue(value=target_chunk_id)
#             )
#         ]
#     ),
#     limit=1,
#     with_payload=True
# )

# # Print the matching record(s)
# if results[0]:
#     for point in results[0]:
#         print(point.payload)
# else:
#     print(f"No record found for chunk_id = {target_chunk_id}")
