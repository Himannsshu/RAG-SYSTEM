import os
import base64
import requests
from PIL import Image
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(BASE_DIR, "nike_shoes.txt")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

IMAGE_URL = "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/252f2db6-d426-4931-80a0-8b7f8f875536/calm-slides-K7mr3W.png"

def download_image(url, filename):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()
    path = os.path.join(IMAGE_DIR, filename)
    with open(path, "wb") as f:
        f.write(response.content)
    return path

def image_to_part(image_path):
    with Image.open(image_path) as img:
        mime = Image.MIME.get(img.format, "image/png")
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
text = TextLoader(TEXT_FILE, encoding="utf-8").load()[0].page_content
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents([text])
vectorstore = FAISS.from_documents(docs, embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"))
retriever = vectorstore.as_retriever()

prompt = ChatPromptTemplate.from_template("{context}\n\n{query}\n\nProvide brief information and store location.")
rag_chain = ({"context": retriever | format_docs, "query": RunnablePassthrough()} | prompt | llm | StrOutputParser())
full_chain = llm | StrOutputParser() | rag_chain
image_path = download_image(IMAGE_URL, "nike3.png")
message = HumanMessage(content=[{"type": "text", "text": "Provide information on given sandal image Brand and model."},image_to_part(image_path),])
print(full_chain.invoke([message]))