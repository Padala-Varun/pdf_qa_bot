📄 DocuChat AI
Ask questions about your documents using AI. With memory. With style.

🧠 What is DocuChat AI?
DocuChat AI is a powerful RAG-based (Retrieval-Augmented Generation) Streamlit application that lets you:

🗂️ Upload PDF, DOCX, or TXT files

❓ Ask questions about their content

💬 Maintain conversational memory (context-aware answers)

🧠 Powered by Gemini 1.5 Pro via LangChain

💾 Runs locally, fully interactive, deployable on Streamlit Cloud

🚀 Features
Feature Description
📄 Multi-format upload PDF, DOCX, TXT support
🔍 RAG pipeline Vector search + LLM response
💭 Contextual memory Remembers previous 5 conversation turns
✨ Gemini 1.5 Pro integration Google GenAI for chat + embeddings
⚡ Fast and accurate Optimized with FAISS and chunked retrieval
🧼 Clear memory button Reset conversation without re-uploading
🧠 Source-aware answers View retrieved document snippets
🎨 Beautiful UI Fully styled with advanced custom CSS

🧪 Tech Stack
LangChain (ConversationalRetrievalChain, FAISS)

Google Gemini 1.5 Pro (via langchain_google_genai)

FAISS for vector storage

Streamlit UI

Python (3.10+ recommended)

🛠️ Installation & Setup

1. Clone the repository

git clone
cd docuchat-ai

2. Install dependencies

pip install -r requirements.txt

3. Set up your environment
   Create a .env file in the root with your Google Generative AI API Key:

GOOGLE_API_KEY=your_google_generative_ai_key_here

Get one here: https://makersuite.google.com/app/apikey

4. Run the app

streamlit run app.py
