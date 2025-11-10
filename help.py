import os
import json
import requests
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials

# Load your credentials
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID","8rMWiSBEsD08dBlQJiBczcymzNTAhDOyeDxjiIgb")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY","8rMWiSBEsD08dBlQJiBczcymzNTAhDOyeDxjiIgb")
region = "us-east-1"  # or your Bedrock region

credentials = Credentials(aws_access_key_id, aws_secret_access_key)

# Bedrock model endpoint
url = "https://bedrock-runtime.us-east-1.amazonaws.com/models/anthropic.claude-v2/invoke"

# Request payload
payload = {"inputText": "Say hello!"}

# Prepare signed request
request = AWSRequest(method="POST", url=url, data=json.dumps(payload),
                     headers={"Content-Type": "application/json"})
SigV4Auth(credentials, "bedrock", region).add_auth(request)

# Send request
response = requests.post(url, headers=dict(request.headers), data=json.dumps(payload))
print(response.json())

