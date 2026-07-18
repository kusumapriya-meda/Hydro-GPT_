# HYDRO GPT

HYDRO GPT is a fully local, offline-ready RAG-based chatbot for water resources and water-related questions. It uses Streamlit for the chat UI, FAISS for vector search, sentence-transformers for embeddings, and Ollama for local inference with a small language model.

## Features

- Ask questions about water scarcity, floods, droughts, groundwater, surface water, pollution, water quality, WASH, and sustainable water management
- Use a curated knowledge base of PDFs and text documents
- Retrieve relevant passages through FAISS vector search
- Generate responses locally with Ollama using a small language model
- Re-index the knowledge base from the Streamlit interface

## Tech stack

- Streamlit for the web UI
- Python for the backend
- FAISS for vector search
- sentence-transformers for document embeddings
- Ollama for local LLM inference
- PyPDF for PDF ingestion

## Project structure

```text
hydro_gpt_gradio/
  README.md
  .gitignore
  requirements.txt
  knowledge_base/
  src/
    __init__.py
    rag_engine.py
    config.py
    prompts.py
    app.py
  scripts/
    __init__.py
    ingest_documents.py
```

## Setup

1. Install Ollama from https://ollama.com
2. Pull a small language model:

```bash
ollama pull llama3.2:3b
```

3. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

4. Add PDFs to the knowledge base folder:

```text
knowledge_base/
```

5. Build the vector index:

```bash
python -m scripts.ingest_documents
```

6. Launch the Streamlit app:

```bash
streamlit run src/app.py
```

## Using a Small Language Model (SLM)

This project is designed to run on laptops with 8GB RAM using small models via Ollama. SLMs are lighter and faster, though they may provide shorter or simpler answers.

Example models:
- llama3.2:3b
- phi3
- qwen2.5:3b
- gemma2:2b
- tinyllama

Example commands:

```bash
ollama pull llama3.2:3b
```

Set the model in your environment or .env file:

```env
OLLAMA_MODEL_NAME=llama3.2:3b
```

## How to add documents

Place PDF files in the knowledge base folder before running the ingestion script or re-indexing from the app. The app will automatically use the documents in that folder.

## Notes

- No paid API keys are required.
- The system works fully offline after the initial model download.
- If Ollama is not running, the app will report a helpful error message.
