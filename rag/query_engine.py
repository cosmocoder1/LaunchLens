"""RAG query interface for LaunchLens.

Loads a persisted ChromaDB vector store and enables semantic querying
of embedded analysis outputs using OpenAI's GPT-3.5/4.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from core.logging import LOGGER

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = Path("chroma_store")

if not OPENAI_API_KEY:
    LOGGER("🔒 OpenAI API key not found. Query functionality will be disabled.")


def query_launchlens(question: str, model_name: str = "gpt-3.5-turbo") -> str | None:
    """Answers a user question based on embedded LaunchLens content using a RAG pipeline.

    Args:
        question (str): The user’s natural language query.
        model_name (str): OpenAI model to use (default: gpt-3.5-turbo)

    Returns:
        Optional[str]: LLM-generated answer, or None if OpenAI key is not configured.
    """
    if not OPENAI_API_KEY:
        return None

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)

    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name=model_name, temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

    response = qa_chain.invoke({"query": question})

    return response["result"]
