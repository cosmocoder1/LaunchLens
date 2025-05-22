"""RAG indexing pipeline for LaunchLens

Embeds CSV summaries and markdown reports into a ChromaDB vector store
to support natural language querying via LLMs.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.document_loaders import TextLoader, CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from core.logging import LOGGER

# Load OpenAI key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in .env")

# Paths
DATA_DIR = Path("analysis/plots")
CHROMA_DIR = Path("chroma_store")


def build_vector_store():
    """
    Loads analysis outputs (CSV and markdown files), converts them into
    semantically meaningful document chunks, and embeds them into a
    persistent ChromaDB vector store using OpenAI embeddings.

    The resulting store enables natural language querying of LaunchLens
    analytics through a Retrieval-Augmented Generation (RAG) pipeline.

    Files indexed:
        - launch_recommendation.md
        - top_launchpad_configs.csv
        - orbit_mass_profiles.csv
        - success_by_year.csv

    Raises:
        ValueError: If OpenAI API key is not configured in the environment.

    Returns:
        None
    """
    LOGGER.info("📦 Building vector store from analysis outputs...")

    loaders = [
        TextLoader(str(DATA_DIR / "launch_recommendation.md")),
        CSVLoader(file_path=str(DATA_DIR / "top_launchpad_configs.csv")),
        CSVLoader(file_path=str(DATA_DIR / "orbit_mass_profiles.csv")),
        CSVLoader(file_path=str(DATA_DIR / "success_by_year.csv")),
    ]

    all_docs = []
    for loader in loaders:
        all_docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(all_docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        split_docs,
        embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    LOGGER.info("✅ ChromaDB vector store built and saved to ./chroma_store")


if __name__ == "__main__":
    build_vector_store()
