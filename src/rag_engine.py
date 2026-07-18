from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import faiss
import numpy as np
import requests
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL_NAME, KNOWLEDGE_BASE_PATH, OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, VECTOR_STORE_PATH
from src.prompts import build_prompt


@dataclass
class Document:
    """Minimal document container for the local RAG pipeline."""

    page_content: str
    metadata: Dict[str, Any]


class RAGEngine:
    """Simple local RAG pipeline for HYDRO GPT."""

    def __init__(self, embedding_model_name: str = EMBEDDING_MODEL_NAME) -> None:
        self.embedding_model_name = embedding_model_name
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def _split_text(self, text: str, chunk_size: int = 400, chunk_overlap: int = 80) -> List[str]:
        """Split text into smaller chunks tuned for small language models and limited RAM."""
        if not text.strip():
            return []

        words = text.split()
        if len(words) <= chunk_size:
            return [text]

        chunks: List[str] = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_words = words[start:end]
            if chunk_words:
                chunks.append(" ".join(chunk_words))
            if end == len(words):
                break
            start = max(0, end - chunk_overlap)
        return chunks

    def load_documents(self, folder_path: Optional[str] = None) -> List[Document]:
        """Load PDF documents from the provided folder path."""
        target_folder = Path(folder_path or KNOWLEDGE_BASE_PATH)
        documents: List[Document] = []

        if not target_folder.exists():
            return documents

        for file_path in sorted(target_folder.glob("*.pdf")):
            try:
                reader = PdfReader(str(file_path))
                text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
                if not text.strip():
                    continue
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": str(file_path), "title": file_path.stem},
                    )
                )
            except Exception as exc:
                print(f"Could not read {file_path}: {exc}")

        return documents

    def create_vector_store(
        self,
        documents: List[Document],
        persist_path: Optional[str] = None,
        embedding_model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Chunk, embed, and persist a FAISS vector store."""
        if not documents:
            raise ValueError("No documents available for indexing.")

        embedding_model_name = embedding_model_name or self.embedding_model_name
        self.embedding_model = SentenceTransformer(embedding_model_name)

        chunks: List[str] = []
        metadata: List[Dict[str, Any]] = []
        for doc in documents:
            split_texts = self._split_text(doc.page_content)
            for chunk_text in split_texts:
                chunks.append(chunk_text)
                metadata.append({**doc.metadata, "content": chunk_text})

        if not chunks:
            raise ValueError("No chunks were created from the provided documents.")

        embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
        embeddings = np.array(embeddings).astype("float32")

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        target_path = Path(persist_path or VECTOR_STORE_PATH)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(index, str(target_path / "index.faiss"))
        np.save(str(target_path / "chunks.npy"), np.array(chunks, dtype=object))
        np.save(str(target_path / "metadata.npy"), np.array(metadata, dtype=object))
        np.save(str(target_path / "embeddings.npy"), embeddings)

        return {
            "num_documents": len(documents),
            "num_chunks": len(chunks),
            "persist_path": str(target_path),
        }

    def load_vector_store(self, persist_path: Optional[str] = None) -> Tuple[faiss.Index, List[str], List[Dict[str, Any]], np.ndarray]:
        """Load an existing FAISS index and chunk metadata."""
        target_path = Path(persist_path or VECTOR_STORE_PATH)
        index_path = target_path / "index.faiss"
        chunks_path = target_path / "chunks.npy"
        metadata_path = target_path / "metadata.npy"
        embeddings_path = target_path / "embeddings.npy"

        if not index_path.exists() or not chunks_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(f"Vector store not found at {target_path}")

        index = faiss.read_index(str(index_path))
        chunks = [str(item) for item in np.load(chunks_path, allow_pickle=True)]
        metadata = [dict(item) for item in np.load(metadata_path, allow_pickle=True)]
        embeddings = np.load(embeddings_path, allow_pickle=True)
        return index, chunks, metadata, embeddings

    def get_retriever(self, vector_store: Tuple[faiss.Index, List[str], List[Dict[str, Any]], np.ndarray], k: int = 4) -> Any:
        """Return a retrieval function for top-k matching chunks."""
        index, chunks, metadata, _ = vector_store

        def retrieve(query: str) -> List[Dict[str, Any]]:
            query_embedding = self.embedding_model.encode([query], show_progress_bar=False).astype("float32")
            _, indices = index.search(query_embedding, min(k, len(chunks)))
            results: List[Dict[str, Any]] = []
            for idx in indices[0]:
                if idx < 0:
                    continue
                results.append({"content": chunks[int(idx)], "metadata": metadata[int(idx)]})
            return results

        return retrieve

    def generate_answer(
        self,
        query: str,
        retriever: Any,
        ollama_base_url: str = OLLAMA_BASE_URL,
        ollama_model: str = OLLAMA_MODEL_NAME,
        system_prompt: str = "",
    ) -> Tuple[str, List[str]]:
        """Generate an answer using retrieved context and a compact prompt for Ollama."""
        retrieved_items = retriever(query)
        context_chunks = [item.get("content", "") for item in retrieved_items if item.get("content")]
        sources = []
        for item in retrieved_items:
            title = item.get("metadata", {}).get("title")
            if title and title not in sources:
                sources.append(title)

        if not context_chunks:
            return (
                "The available documents do not have enough information on this.",
                [],
            )

        context_text = "\n\n".join(context_chunks)
        prompt = build_prompt(context_text, query)

        payload = {
            "model": ollama_model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }

        try:
            response = requests.post(f"{ollama_base_url}/api/chat", json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            answer_text = result.get("message", {}).get("content", "")
            return answer_text.strip(), sources
        except requests.RequestException as exc:
            return f"Ollama request failed: {exc}", sources
