import re
import streamlit as st
import os
import tempfile

st.set_page_config(page_title="Luminary", layout="centered")

from ingest import load_and_chunk
from embeddings import create_vector_store
from qa_chain import create_qa_chain

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")

st.title("✨ Luminary")
st.write("Upload a document and get instant answers powered by AI.")

uploaded_file = st.file_uploader("Upload your document (max 10 MB)", type=["pdf", "txt", "docx", "csv"])

if uploaded_file is not None and uploaded_file.size > 10 * 1024 * 1024:
    st.error("File too large! Please upload a file smaller than 10 MB.")
    uploaded_file = None

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    with st.spinner("Reading and processing your document..."):
        chunks = load_and_chunk(tmp_path, file_type)
        

    if len(chunks) == 0:
        st.error("Could not read the document. Please try a different file.")
    else:
        with st.spinner("Building knowledge base..."):
            vector_store = create_vector_store(chunks)
            qa_chain = create_qa_chain(vector_store)

        st.success("Document ready! Ask your questions below.")

        question = st.text_input("Ask a question about your document:")

        if question:
            with st.spinner("Thinking..."):
                try:
                    answer = qa_chain.invoke(question)
                    st.write("### Answer")
                    st.markdown(answer)
                except Exception as e:
                    st.error("Something went wrong. Please try again in a moment.")

    os.unlink(tmp_path)
