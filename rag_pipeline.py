import os
from dotenv import load_dotenv
import nest_asyncio

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
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

# ✅ Create RAG ConversationalRetrievalChain with Memory
def get_qa_chain_with_memory(vectorstore):
    # Create memory that remembers last 5 conversation turns
    memory = ConversationBufferWindowMemory(
        k=5,  # Remember last 5 exchanges
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}  # Retrieve top 4 relevant chunks
    )
    
    # Use ConversationalRetrievalChain for memory support
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False,
        chain_type="stuff"
    )
    
    return chain

# ✅ Legacy function for backward compatibility
def get_qa_chain(vectorstore):
    """Legacy function - redirects to memory-enabled version"""
    return get_qa_chain_with_memory(vectorstore)

# ✅ Clear conversation memory
def clear_memory(qa_chain):
    """Clear the conversation memory"""
    if hasattr(qa_chain, 'memory'):
        qa_chain.memory.clear()
        return True
    return False

# ✅ Get conversation history
def get_conversation_history(qa_chain):
    """Get the current conversation history"""
    if hasattr(qa_chain, 'memory') and hasattr(qa_chain.memory, 'chat_memory'):
        messages = qa_chain.memory.chat_memory.messages
        history = []
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                human_msg = messages[i].content
                ai_msg = messages[i + 1].content
                history.append({"question": human_msg, "answer": ai_msg})
        return history
    return []