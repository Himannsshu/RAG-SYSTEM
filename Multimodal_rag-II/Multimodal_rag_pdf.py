import base64
import os
import sys
import fitz
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

PDF_FILE = "rag_system.pdf"
CHAT_MODEL = "gemini-2.5-flash"
DB_FOLDER = "chroma_db"

api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, google_api_key=api_key, temperature=0) | StrOutputParser()
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)

def load_pages(pdf_file):
    pages = []
    doc = fitz.open(pdf_file)
    for page in doc:
        pix = page.get_pixmap(dpi=100)
        image = base64.b64encode(pix.tobytes("png")).decode("utf-8")
        pages.append({"text": page.get_text(), "image": image})
    return pages

def image_block(b64_image):
    return {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}

def get_vector_store(pages):

    vector_store = Chroma(collection_name="pdf_pages",embedding_function=embeddings,persist_directory=DB_FOLDER)
    if len(vector_store.get()["ids"]) == 0:
        texts = []
        for i, page in enumerate(pages):
            text = page["text"][:6000].strip()
            texts.append(text if text else f"Page {i + 1} (only an image)")
        metadatas = [{"page": i} for i in range(len(pages))]
        vector_store.add_texts(texts, metadatas=metadatas)
    return vector_store

def ask(question, vector_store, pages, top_k=2):
    results = vector_store.similarity_search(question, k=top_k)
    content = []
    page_text = ""
    used_pages = []
    for result in results:
        n = result.metadata["page"]
        used_pages.append(n + 1)
        page_text += f"\n Page {n + 1} \n{pages[n]['text']}"
        content.append(image_block(pages[n]["image"]))
    content.append({
        "type": "text",
        "text": "Answer the question using only the pages given.\n\n"
                f"Question: {question}\n\nPage text:{page_text}",
    })
    answer = llm.invoke([HumanMessage(content=content)])
    return answer, used_pages

def main():
    pages = load_pages(PDF_FILE)
    print(f"Loaded {len(pages)} pages from {PDF_FILE}")
    vector_store = get_vector_store(pages)
    print("Ready!")

    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()
        if question.lower() in ("exit", "quit", ""):
            break
        try:
            answer, used_pages = ask(question, vector_store, pages)
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print(f"\nGemini quota is finished for {CHAT_MODEL}. "
                      "Change CHAT_MODEL at the top of the file or try again after the quota resets.")
                continue
            raise
        print("\n" + answer)
        print(f"\n(Answer taken from page(s): {', '.join(map(str, used_pages))})")

if __name__ == "__main__":
    main()