from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def get_chunk_settings(file_path):
    file_size = os.path.getsize(file_path)  # in bytes
    
    if file_size < 5_000:            # < 5KB (~1-2 sec)
        return 50, 5
    elif file_size < 10_000:         # 5KB - 10KB (~2-3 sec)
        return 100, 10
    elif file_size < 25_000:         # 10KB - 25KB (~3-4 sec)
        return 150, 15
    elif file_size < 50_000:         # 25KB - 50KB (~4-5 sec)
        return 200, 20
    elif file_size < 100_000:        # 50KB - 100KB (~5-8 sec)
        return 300, 30
    elif file_size < 250_000:        # 100KB - 250KB (~8-10 sec)
        return 400, 40
    elif file_size < 500_000:        # 250KB - 500KB (~10-15 sec)
        return 500, 50
    elif file_size < 1_000_000:      # 500KB - 1MB (~15-20 sec)
        return 600, 60
    elif file_size < 2_000_000:      # 1MB - 2MB (~20-25 sec)
        return 800, 80
    elif file_size < 5_000_000:      # 2MB - 5MB (~25-30 sec)
        return 1200, 120
    elif file_size < 10_000_000:     # 5MB - 10MB (~30-35 sec)
        return 1800, 180
    else:                             # > 10MB (too large, warn user)
        return 2500,250

def load_and_chunk(file_path, file_type):
    if file_type == "pdf":
        loader = PyPDFLoader(file_path)
    elif file_type == "txt":
        loader = TextLoader(file_path)
    elif file_type == "docx":
        loader = UnstructuredWordDocumentLoader(file_path)
    elif file_type == "csv":
        loader = CSVLoader(file_path)
    
    documents = loader.load()
    
    chunk_size, chunk_overlap = get_chunk_settings(file_path)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = splitter.split_documents(documents)
    return chunks
