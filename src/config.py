import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# Small language model for modest hardware; change OLLAMA_MODEL_NAME to other SLMs such as phi3, qwen2.5:3b, gemma2:2b, or tinyllama.
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3.2:3b")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", str(BASE_DIR / "data" / "vectorstore"))
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", str(BASE_DIR / "knowledge_base"))
