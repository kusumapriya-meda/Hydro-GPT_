import sys
import time
from pathlib import Path
from typing import Any, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import requests
import streamlit as st

try:
    from src.config import KNOWLEDGE_BASE_PATH, OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, VECTOR_STORE_PATH
    from src.rag_engine import RAGEngine
except ImportError:
    from config import KNOWLEDGE_BASE_PATH, OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, VECTOR_STORE_PATH
    from rag_engine import RAGEngine


@st.cache_resource(show_spinner=False)
def get_engine() -> RAGEngine:
    """Create a single shared RAG engine instance for the app."""
    return RAGEngine()


@st.cache_data(show_spinner=False)
def load_documents_cached(folder_path: str) -> List[Any]:
    """Cache PDF loading so the app does not re-read documents on every rerun."""
    return get_engine().load_documents(folder_path)


def clear_caches() -> None:
    """Clear cached document and vector-store data after rebuilds or uploads."""
    st.cache_data.clear()
    st.session_state.pop("vector_store", None)
    st.session_state.pop("retriever", None)


def check_ollama_status() -> bool:
    """Check whether the local Ollama server is reachable."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        return response.ok
    except requests.RequestException:
        return False


def get_knowledge_base_summary() -> Tuple[int, int, bool]:
    """Return document count, chunk count, and vector-store availability."""
    documents = load_documents_cached(KNOWLEDGE_BASE_PATH)
    pdf_count = len(documents)
    chunk_count = 0
    vector_loaded = False

    if "vector_store" in st.session_state and st.session_state.vector_store is not None:
        _, chunks, _, _ = st.session_state.vector_store
        chunk_count = len(chunks)
        vector_loaded = True
    else:
        store_path = Path(VECTOR_STORE_PATH)
        if (store_path / "index.faiss").exists():
            try:
                _, chunks, _, _ = get_engine().load_vector_store(VECTOR_STORE_PATH)
                chunk_count = len(chunks)
                vector_loaded = True
            except Exception:
                chunk_count = 0
                vector_loaded = False

    return pdf_count, chunk_count, vector_loaded


def ensure_vector_store() -> None:
    """Create the vector store automatically if it does not exist yet."""
    store_path = Path(VECTOR_STORE_PATH)
    if (store_path / "index.faiss").exists():
        if "vector_store" not in st.session_state or st.session_state.vector_store is None:
            try:
                st.session_state.vector_store = get_engine().load_vector_store(VECTOR_STORE_PATH)
                st.session_state.retriever = get_engine().get_retriever(st.session_state.vector_store, k=2)
            except Exception:
                st.session_state.vector_store = None
        return

    try:
        documents = load_documents_cached(KNOWLEDGE_BASE_PATH)
        if documents:
            get_engine().create_vector_store(documents, persist_path=VECTOR_STORE_PATH)
            st.session_state.vector_store = get_engine().load_vector_store(VECTOR_STORE_PATH)
            st.session_state.retriever = get_engine().get_retriever(st.session_state.vector_store, k=2)
    except Exception as exc:
        print(f"Initial indexing failed: {exc}")


def ingest_documents() -> Tuple[str, int, int]:
    """Rebuild the FAISS index from the knowledge base."""
    documents = load_documents_cached(KNOWLEDGE_BASE_PATH)
    if not documents:
        return "No documents found.", 0, 0

    try:
        with st.status("Indexing Started...", expanded=True) as status:
            status.write("Loading documents...")
            status.write("Generating embeddings...")
            status.write("Building FAISS index...")
            stats = get_engine().create_vector_store(documents, persist_path=VECTOR_STORE_PATH)
            status.write(f"Number of PDFs: {stats['num_documents']}")
            status.write(f"Number of chunks created: {stats['num_chunks']}")
            status.update(label="Completed Successfully", state="complete", expanded=False)
        clear_caches()
        st.session_state.vector_store = get_engine().load_vector_store(VECTOR_STORE_PATH)
        st.session_state.retriever = get_engine().get_retriever(st.session_state.vector_store, k=2)
        return "Completed Successfully", stats["num_documents"], stats["num_chunks"]
    except Exception as exc:
        return f"Indexing failed: {exc}", 0, 0


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
        clear_caches()
        return f"Saved {len(saved_files)} file(s). Rebuild the knowledge base when ready."
    return "No files were uploaded."


def render_sidebar() -> None:
    """Render a polished sidebar with status and example questions."""
    with st.sidebar:
        st.markdown("### 💧 Hydro GPT")
        st.caption("OFFLINE WATER ASSISTANT")

        pdf_count, chunk_count, vector_loaded = get_knowledge_base_summary()
        ollama_running = check_ollama_status()
        is_ready = ollama_running and vector_loaded
        status_emoji = "🟢" if is_ready else "🔴"
        status_text = "Ready" if is_ready else "Offline"

        st.markdown("---")
        st.markdown("### Status")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(status_emoji)
        with col2:
            st.write(status_text)

        st.markdown("**Documents**")
        st.write(f"{pdf_count}")
        st.markdown("**Chunks**")
        st.write(f"{chunk_count}")
        st.markdown("**Model**")
        st.write(f"`{OLLAMA_MODEL_NAME}`")

        st.markdown("---")
        st.markdown("### Example Questions")
        example_questions = [
            "Water quality standards",
            "Causes of flooding",
            "Groundwater depletion",
            "Pollution sources",
            "Drought management",
            "Rainwater harvesting",
        ]
        for question in example_questions:
            if st.button(question, use_container_width=True, key=f"q_{question}"):
                st.session_state.pending_prompt = question
                st.rerun()

        st.markdown("---")
        if st.button("Rebuild knowledge base", use_container_width=True):
            status_text, num_docs, num_chunks = ingest_documents()
            st.success(status_text)
            if num_docs or num_chunks:
                st.info(f"Documents: {num_docs} | Chunks: {num_chunks}")
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("pending_prompt", None)
            st.rerun()
            st.write("• Ollama")


def render_chat_history() -> None:
    """Render stored chat messages with sources and timing information."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                deduped_sources = message.get("sources", [])
                if deduped_sources:
                    source_count = len(deduped_sources)
                    st.markdown(f"<span style='color: #20C997; font-size: 0.85rem;'>from {source_count} document{'s' if source_count != 1 else ''}</span>", unsafe_allow_html=True)
                if message.get("response_time") is not None:
                    st.caption(f"Response Time: {message['response_time']:.2f} seconds")


def render_header() -> None:
    """Render the top-level header and decorative separator."""
    st.title("💧 Hydro GPT")
    st.caption("Ask about water resources, pollution, floods, drought and sustainability.")
    st.markdown("<svg viewBox='0 0 1200 120' preserveAspectRatio='none' style='display: block; width: 100%; height: 40px; margin: -10px 0 20px 0;'><polyline points='0,50 150,25 300,50 450,25 600,50 750,25 900,50 1050,25 1200,50 1200,120 0,120' fill='none' stroke='currentColor' opacity='0.2' stroke-width='2'/></svg>", unsafe_allow_html=True)


def main() -> None:
    """Launch the Streamlit chat UI."""
    st.set_page_config(page_title="HYDRO GPT", page_icon="💧", layout="wide")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = ""

    render_sidebar()
    render_header()
    ensure_vector_store()

    render_chat_history()

    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = ""
    else:
        prompt = st.chat_input("Ask a water-related question")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        pdf_count, _, vector_loaded = get_knowledge_base_summary()
        if not pdf_count:
            fallback = "No documents found."
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback, "sources": [], "response_time": 0.0})
            return

        if not check_ollama_status():
            fallback = "Ollama is not running. Please start Ollama to continue."
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback, "sources": [], "response_time": 0.0})
            return

        if not vector_loaded:
            fallback = "Knowledge Base not indexed."
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback, "sources": [], "response_time": 0.0})
            return

        try:
            vector_store = st.session_state.get("vector_store")
            if vector_store is None:
                vector_store = get_engine().load_vector_store(VECTOR_STORE_PATH)
                st.session_state.vector_store = vector_store
            retriever = st.session_state.get("retriever")
            if retriever is None:
                retriever = get_engine().get_retriever(vector_store, k=2)
                st.session_state.retriever = retriever

            start_time = time.perf_counter()
            answer, sources = get_engine().generate_answer(
                query=prompt,
                retriever=retriever,
                ollama_base_url=OLLAMA_BASE_URL,
                ollama_model=OLLAMA_MODEL_NAME,
            )
            response_time = time.perf_counter() - start_time
            deduped_sources = list(dict.fromkeys(sources))

            with st.chat_message("assistant"):
                st.markdown(answer)
                if deduped_sources:
                    source_count = len(deduped_sources)
                    st.markdown(f"<span style='color: #20C997; font-size: 0.85rem;'>from {source_count} document{'s' if source_count != 1 else ''}</span>", unsafe_allow_html=True)
                st.caption(f"Response Time: {response_time:.2f} seconds")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": deduped_sources,
                "response_time": response_time,
            })
        except FileNotFoundError:
            fallback = "Knowledge Base not indexed."
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback, "sources": [], "response_time": 0.0})
        except Exception as exc:
            fallback = f"An error occurred: {exc}"
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback, "sources": [], "response_time": 0.0})


if __name__ == "__main__":
    main()
