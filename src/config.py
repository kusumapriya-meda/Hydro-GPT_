import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

def get_secret(key: str, default: str) -> str:
    """Helper to check os.environ first, then streamlit st.secrets, then default."""
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default

OLLAMA_BASE_URL = get_secret("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL_NAME = get_secret("OLLAMA_MODEL_NAME", "llama3.2:3b")
EMBEDDING_MODEL_NAME = get_secret("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
VECTOR_STORE_PATH = get_secret("VECTOR_STORE_PATH", str(BASE_DIR / "data" / "vectorstore"))
KNOWLEDGE_BASE_PATH = get_secret("KNOWLEDGE_BASE_PATH", str(BASE_DIR / "knowledge_base"))
