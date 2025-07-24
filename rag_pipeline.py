import os
from dotenv import load_dotenv
import nest_asyncio

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

# Fix asyncio issue for Gemini's async client
nest_asyncio.apply()

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# ✅ Initialize Gemini 1.5 Pro for Chat (LLM)
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro",
    google_api_key=api_key,
    temperature=0.3,
    convert_system_message_to_human=True
)

# ✅ Initialize Google Embeddings
def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )

embeddings = get_embeddings()

# ✅ Split input into chunks and build vector store
def create_vectorstore(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.create_documents([text])
    return FAISS.from_documents(docs, embeddings)

# ✅ Create RAG RetrievalQA Chain
def get_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
