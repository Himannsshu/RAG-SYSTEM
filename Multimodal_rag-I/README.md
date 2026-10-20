# Multimodal RAG System with Gemini & LangChain

A Python-based **Retrieval-Augmented Generation (RAG)** pipeline that combines local text document retrieval with multimodal image analysis. This system uses a query-rewriting agent to inspect product images, convert visual inputs into searchable text queries, retrieve relevant context from a FAISS vector database, and generate accurate answers with store locations using Google's Gemini models.

## Features

- **Multimodal Inputs:** Pass images alongside text queries to visually search your knowledge base.
- **Query Rewriting / Expansion:** Uses an initial LLM pass to translate visual or messy user input into clean, optimized search queries.
- **Local Vector Storage:** Powered by **FAISS** for fast similarity search over embedded text chunks.
- **LangChain Expression Language (LCEL):** Built using modern LangChain pipe operators (`|`) for clean, modular data pipelines.
- **Robust Text Splitting:** Utilizes `RecursiveCharacterTextSplitter` to chunk source documents effectively.
