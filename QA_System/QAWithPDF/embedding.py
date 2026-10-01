import sys
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from exception import customexception
from logger import logging

def download_gemini_embedding(model, document):
    """Initializes an embedding model and returns a query engine."""
    try:
        logging.info("Initializing local HuggingFace embedding model...")
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.llm = model
        Settings.embed_model = embed_model
        Settings.chunk_size = 800
        Settings.chunk_overlap = 20
        logging.info("Creating vector store index from documents...")
        index = VectorStoreIndex.from_documents(document)
        index.storage_context.persist()
        logging.info("Creating query engine...")
        query_engine = index.as_query_engine()
        return query_engine
    except Exception as e:
        raise customexception(e, sys)