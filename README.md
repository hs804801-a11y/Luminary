# Luminary
### Document Question Answering System using Retrieval-Augmented Generation (RAG)

---

## What is Luminary?

Luminary is a web application that lets you upload any document and ask questions about it in plain English. Instead of reading through the entire document yourself, Luminary extracts the relevant information and gives you precise, well-formatted answers — powered by a Large Language Model and RAG architecture.

**Live Demo:** https://happy5352m-luminary.hf.space

---

## What is RAG?

RAG (Retrieval-Augmented Generation) is an AI architecture that solves a key limitation of LLMs — they can hallucinate or give outdated answers because they rely only on their training data.

RAG fixes this by:
1. Taking your document and breaking it into small chunks
2. Converting those chunks into vector embeddings (numerical representations)
3. When you ask a question, finding the most relevant chunks using similarity search
4. Passing only those relevant chunks to the LLM as context
5. The LLM answers based on your document, not its training data

This means answers are accurate, grounded, and specific to your document.

---

## How It Works

### Step 1 — Document Ingestion (ingest.py)
The uploaded document is loaded using the appropriate loader based on file type. It is then split into chunks using RecursiveCharacterTextSplitter. Chunk size is dynamically adjusted based on file size — smaller files get smaller chunks for precision, larger files get bigger chunks for performance.

### Step 2 — Embeddings and Vector Store (embeddings.py)
Each chunk is converted into a vector embedding using the HuggingFace sentence-transformers model (all-MiniLM-L6-v2) running locally on CPU. These embeddings are stored in a FAISS vector store for fast similarity search.

### Step 3 — Question Answering (qa_chain.py)
When the user asks a question, the retriever finds the most relevant chunks from the vector store. These chunks are passed as context to the LLM (LLaMA 3.3 70B via Groq API) along with the question. The LLM generates a clear, well-formatted answer based only on the provided context.

### Step 4 — UI (app.py)
The Streamlit interface handles file upload, processing, and question input. It shows spinners during processing and renders the final answer with proper markdown formatting.

---

## Architecture

User uploads document
↓
Document Loader (PDF / TXT / DOCX / CSV)
↓
Text Splitter (dynamic chunk sizing)
↓
HuggingFace Embeddings (all-MiniLM-L6-v2)
↓
FAISS Vector Store
↓
User asks a question
↓
Similarity Search (retrieve relevant chunks)
↓
LLM (LLaMA 3.3 70B via Groq) + Context
↓
Formatted Answer

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| Document Loading | LangChain Community Loaders |
| Text Splitting | RecursiveCharacterTextSplitter |
| Embeddings | HuggingFace sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS |
| LLM | LLaMA 3.3 70B via Groq API |
| Containerization | Docker |
| Deployment | Hugging Face Spaces |

---

## Supported File Types

- PDF (.pdf)
- Plain Text (.txt)
- Word Document (.docx)
- CSV (.csv)
- Maximum file size: 10 MB

---

## Project Structure

Luminary-RAG/
├── src/
│   ├── app.py              # Streamlit UI and main app logic
│   ├── ingest.py           # Document loading and chunking
│   ├── embeddings.py       # Vector embeddings and FAISS store
│   └── qa_chain.py         # LLM chain and retrieval logic
├── requirements.txt        # Root level dependencies
├── Dockerfile              # Container configuration
├── .env                    # API key (not committed to GitHub)
├── .gitignore
└── README.md

---

## How to Run Locally

### Requirements
- Python 3.10+
- A Groq API key (free at https://console.groq.com)

### Option 1 — Run directly

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/luminary.git
cd luminary
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Create a .env file**

GROQ_API_KEY=your_groq_key_here

**4. Run the app**

```bash
streamlit run src/app.py
```

The app will open at http://localhost:8501

### Option 2 — Run with Docker

**1. Build the image**

```bash
docker build -t luminary .
```

**2. Run the container**

```bash
docker run -p 8501:8501 -e GROQ_API_KEY=your_key_here luminary
```

The app will open at http://localhost:8501

---

## Known Limitations

- Maximum file size is 10 MB
- The app processes one document at a time — uploading a new document replaces the previous one
- Very large documents may take 30-40 seconds to process on first load
- Answers are based strictly on the uploaded document — the LLM will not use outside knowledge

---

## What I Learned

- How RAG (Retrieval-Augmented Generation) works end to end
- How to convert documents into vector embeddings using HuggingFace sentence-transformers
- How to build and query a FAISS vector store for semantic similarity search
- How to build a LangChain pipeline combining retrieval and LLM generation
- How to dynamically adjust chunk sizes based on document size for better performance
- How to containerize a Python app using Docker
- How to deploy a Streamlit app on Hugging Face Spaces
