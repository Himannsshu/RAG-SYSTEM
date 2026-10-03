import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

loder=PyPDFLoader('rag_system.pdf')
document=loder.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
text_chunks=text_splitter.split_documents(document)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore=FAISS.from_documents(text_chunks, embeddings)
retriever=vectorstore.as_retriever()
template="""You are an assistant for question-answering tasks.Use the following pieces of retrieved context to answer the question.If you don't know the answer, just say that you don't know.Use ten sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:"""
prompt=ChatPromptTemplate.from_template(template)
output_parser=StrOutputParser()

llm_model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
rag_chain = ({"context": retriever,  "question": RunnablePassthrough()}| prompt| llm_model| output_parser)
rag_chain.invoke("what is rag system")