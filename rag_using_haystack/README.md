AG with Haystack and Gemini

A simple Retrieval-Augmented Generation (RAG) pipeline built with Haystack and Google Gemini. It answers questions about the Seven Wonders of the Ancient World using a Hugging Face dataset.

## How It Works

1. Load the `bilgeyucel/seven-wonders` dataset.
2. Embed the documents with `all-MiniLM-L6-v2` and store them in memory.
3. Retrieve the documents most similar to the question.
4. Send the question and retrieved context to Gemini (`gemini-2.5-flash`) to generate
