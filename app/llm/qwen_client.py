import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_qwen_client():
    global _client
    if _client is None:
        token = os.getenv("HF_TOKEN")
        if not token:
            raise RuntimeError("HF_TOKEN not set")

        _client = InferenceClient(
            model="Qwen/Qwen2.5-Coder-7B-Instruct",
            token=token
        )
    return _client
