from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

def create_qa_chain(vector_store):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    retriever = vector_store.as_retriever()

    prompt = PromptTemplate.from_template(
        "Use the following context to answer the question. "
        "Format your answer clearly and professionally: "
        "- Use proper paragraphs with clear spacing. "
        "- Use numbered steps for multi-step solutions. "
        "- For code or SQL, wrap it in triple backticks like ```sql ... ``` "
        "- Only use LaTeX math ($...$) for actual mathematical expressions. "
        "- Never use LaTeX for code, SQL, or plain text. "
        "- End with a clear final answer.\n\nContext: {context}\n\nQuestion: {question}"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
