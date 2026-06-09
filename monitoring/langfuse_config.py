import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

def get_langfuse_client():
    client = Langfuse(
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        host=os.getenv("LANGFUSE_HOST")
    )
    return client

def trace_event(name: str, input_data: dict, output_data: dict = None, metadata: dict = None):
    try:
        client = get_langfuse_client()
        trace = client.trace(
            name=name,
            input=input_data,
            output=output_data or {},
            metadata=metadata or {}
        )
        return trace
    except Exception as e:
        print(f"[Langfuse Warning] Could not log trace: {e}")
        return None
    