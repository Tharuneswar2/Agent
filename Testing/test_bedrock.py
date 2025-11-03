import boto3

# Create the Bedrock control-plane client (for listing models)
bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")

response = bedrock.list_foundation_models()

for model in response["modelSummaries"]:
    print(model["modelId"], "-", model["providerName"])
