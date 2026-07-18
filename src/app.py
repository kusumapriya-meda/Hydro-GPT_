from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Optional

import streamlit as st

from src.config import KNOWLEDGE_BASE_PATH, OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, VECTOR_STORE_PATH
from src.rag_engine import RAGEngine


engine = RAGEngine()


def ensure_vector_store() -> None:
    """Create the vector store automatically if it does not exist yet."""
    store_path = Path(VECTOR_STORE_PATH)
    if not (store_path / "index.faiss").exists():
        try:
            documents = engine.load_documents(KNOWLEDGE_BASE_PATH)
            if documents:
                engine.create_vector_store(documents, persist_path=VECTOR_STORE_PATH)
        except Exception as exc:
            print(f"Initial indexing failed: {exc}")


def ingest_documents() -> str:
    """Rebuild the FAISS index from the knowledge base."""
    documents = engine.load_documents(KNOWLEDGE_BASE_PATH)
    if not documents:
        return "No PDFs found in the knowledge base. Add PDFs first."
    try:
        stats = engine.create_vector_store(documents, persist_path=VECTOR_STORE_PATH)
        return f"Index rebuilt successfully: {stats['num_documents']} document(s), {stats['num_chunks']} chunk(s)."
    except Exception as exc:
        return f"Indexing failed: {exc}"


def upload_files(uploaded_files: Optional[List[st.runtime.uploaded_file_manager.UploadedFile]]) -> str:
    """Save uploaded PDFs into the knowledge base directory."""
    knowledge_dir = Path(KNOWLEDGE_BASE_PATH)
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    saved_files: List[str] = []
    for uploaded_file in uploaded_files or []:
        if uploaded_file is None:
            continue
        destination = knowledge_dir / uploaded_file.name
        with destination.open("wb") as handle:
            handle.write(uploaded_file.getbuffer())
        saved_files.append(uploaded_file.name)
    if saved_files:
        return f"Saved {len(saved_files)} file(s) to the knowledge base. Click Re-index to rebuild the vector store."
    return "No files were uploaded."


def main() -> None:
    """Launch the Streamlit chat UI."""
    st.set_page_config(page_title="HYDRO GPT", page_icon="💧", layout="wide")
    st.title("HYDRO GPT – RAG-Based Water Assistant")
    st.caption("Ask anything about water: scarcity, pollution, floods, drought, sustainability, policies, and more.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("Knowledge base")
        st.text(f"Ollama URL: {OLLAMA_BASE_URL}")
        st.text(f"Model: {OLLAMA_MODEL_NAME}")
        uploaded_files = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True)
        if st.button("Upload PDFs"):
            status = upload_files(uploaded_files)
            st.success(status)
        if st.button("Re-index knowledge base"):
            status = ingest_documents()
            st.success(status)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a water-related question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        ensure_vector_store()
        try:
            vector_store = engine.load_vector_store(VECTOR_STORE_PATH)
            retriever = engine.get_retriever(vector_store)
            answer, sources = engine.generate_answer(
                query=prompt,
                retriever=retriever,
                ollama_base_url=OLLAMA_BASE_URL,
                ollama_model=OLLAMA_MODEL_NAME,
            )
            if sources:
                source_block = "\n".join([f"- {source}" for source in sources])
                answer = f"{answer}\n\nSources:\n{source_block}"
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except FileNotFoundError:
            fallback = "The vector store does not exist yet. Please re-index the knowledge base first."
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback})
        except Exception as exc:
            fallback = f"An error occurred: {exc}"
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback})


if __name__ == "__main__":
    main()
