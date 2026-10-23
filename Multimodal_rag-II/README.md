# Multimodal PDF RAG with Gemini

Ask questions about a PDF and get answers from Google Gemini, including questions about its **diagrams, tables and figures**, not just the plain text.

Most simple PDF chatbots only read the extracted text, so anything inside a chart or table gets lost. This project keeps every page as both text and an image, finds the pages that match your question, and sends them to Gemini together.

## How it works

1. **Read the PDF.** [PyMuPDF](https://pymupdf.readthedocs.io/) converts each page into its text and a PNG image.
2. **Create embeddings.** The text of each page is embedded with Gemini (`gemini-embedding-001`) and stored in a [Chroma](https://www.trychroma.com/) vector database. This happens only once, because the database is saved to disk.
3. **Search.** When you ask a question, the most similar pages (top 2 by default) are retrieved.
4. **Answer.** The text and images of those pages are sent to a Gemini model (`gemini-2.5-flash` by default), which answers using only what is on the pages. The script also prints which page numbers the answer came from.

## Tech stack

- Python 3.10+
- [LangChain](https://www.langchain.com/) (`langchain-core`, `langchain-chroma`, `langchain-google-genai`)
- Google Gemini API (chat + embeddings)
- ChromaDB
- PyMuPDF
- python-dotenv

## Project structure

```
.
├── Multimodal_rag_pdf.py   # main script
├── rag_system.pdf          # the PDF you want to ask questions about
├── requirements.txt
├── .env                    # your API key (do not upload this to GitHub)
├── chroma_db/              # created automatically on the first run
└── README.md
```

## Good to know

- **Changing the PDF?** Delete the `chroma_db` folder first, otherwise the old embeddings will be reused.
- **API limits.** The free Gemini tier has daily request limits for each model. Every question uses exactly one chat request, so you can ask a limited number of questions per day. If you see a `429 RESOURCE_EXHAUSTED` error, change `CHAT_MODEL` to another model (for example `gemini-2.5-flash-lite`) or wait for the quota to reset. You can check your limits in [Google AI Studio](https://ai.dev/rate-limit).

## Limitations

- Pages are found using their text only, so a page that is just an image (for example a scanned page) is harder to find.
- Only the first 6,000 characters of each page are used to create its embedding.
- Retrieval works per page, so very long pages with many topics can be less precise.
