from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import KNOWLEDGE_BASE_PATH, VECTOR_STORE_PATH
from src.rag_engine import RAGEngine


def main() -> None:
    """Ingest PDFs from the knowledge base and build the FAISS index."""
    engine = RAGEngine()
    documents = engine.load_documents(KNOWLEDGE_BASE_PATH)

    if not documents:
        print("No PDFs were found in the knowledge base. Add one or more PDFs and try again.")
        return

    stats = engine.create_vector_store(documents, persist_path=VECTOR_STORE_PATH)
    print(f"Indexed {stats['num_documents']} document(s) into {stats['num_chunks']} chunk(s).")
    print(f"Vector store saved to {stats['persist_path']}")


if __name__ == "__main__":
    main()
