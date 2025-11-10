import subprocess
import json

class BedrockLLM:
    def __init__(self, model_id: str, region: str = "us-east-1"):
        self.model_id = model_id
        self.region = region

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 512) -> str:
        try:
            cmd = [
                "aws", "bedrock", "invoke-model",
                "--model-id", self.model_id,
                "--body", json.dumps({"inputText": prompt}),
                "--region", self.region
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = json.loads(result.stdout)
            # Output structure: {'body': '{"completion":"..."}', ...}
            if "body" in output:
                body_json = json.loads(output["body"])
                return body_json.get("completion", "")
            return str(output)
        except subprocess.CalledProcessError as e:
            return f"Error calling Bedrock CLI: {e.stderr}"
