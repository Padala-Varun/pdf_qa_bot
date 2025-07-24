import streamlit as st
from loader import load_pdf, load_docx, load_txt
from rag_pipeline import create_vectorstore, get_qa_chain_with_memory, clear_memory, get_conversation_history

# Page configuration
st.set_page_config(
    page_title="DocuChat AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for memory and chat history
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main background and font */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, rgba(26, 35, 126, 0.9) 0%, rgba(74, 20, 140, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(100, 200, 255, 0.3);
        text-align: center;
    }
    
    .main-title {
        color: #64FFDA;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        color: #B39DDB;
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* Card styling */
    .upload-card, .question-card, .answer-card, .chat-history-card {
        background: linear-gradient(135deg, rgba(33, 33, 33, 0.95) 0%, rgba(48, 48, 48, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(100, 200, 255, 0.2);
        color: #E8EAF6;
    }
    
    .upload-card {
        border-left: 5px solid #00E676;
    }
    
    .question-card {
        border-left: 5px solid #00BCD4;
    }
    
    .answer-card {
        border-left: 5px solid #FF6D00;
        background: linear-gradient(135deg, rgba(26, 35, 126, 0.9) 0%, rgba(142, 36, 170, 0.9) 100%);
        color: #E1F5FE;
    }
    
    .chat-history-card {
        border-left: 5px solid #9C27B0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    /* Chat message styling */
    .chat-message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 3px solid #64FFDA;
        background: rgba(55, 71, 79, 0.5);
    }
    
    .user-question {
        color: #64FFDA;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .ai-answer {
        color: #E8EAF6;
        line-height: 1.6;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div > div {
        background: linear-gradient(135deg, #37474F 0%, #546E7A 100%);
        border-radius: 10px;
        border: 2px dashed #64FFDA;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #455A64;
        padding: 10px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: rgba(55, 71, 79, 0.9);
        color: #E8EAF6;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00BCD4;
        box-shadow: 0 0 10px rgba(0, 188, 212, 0.4);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00BCD4 0%, #0097A7 100%);
        color: #E8F5E8;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 188, 212, 0.4);
        background: linear-gradient(135deg, #00ACC1 0%, #00838F 100%);
    }
    
    /* Clear button styling */
    .clear-button {
        background: linear-gradient(135deg, #FF5722 0%, #D84315 100%) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(55, 71, 79, 0.8) 0%, rgba(69, 90, 100, 0.8) 100%);
        border-radius: 10px;
        color: #64FFDA;
        font-weight: 600;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 230, 118, 0.2) 0%, rgba(46, 125, 50, 0.2) 100%);
        border-left: 5px solid #00E676;
        border-radius: 10px;
        color: #C8E6C9;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.2) 0%, rgba(198, 40, 40, 0.2) 100%);
        border-left: 5px solid #FF5252;
        border-radius: 10px;
        color: #FFCDD2;
    }
    
    /* Spinner styling */
    .stSpinner {
        color: #64FFDA;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(55, 71, 79, 0.9) 0%, rgba(69, 90, 100, 0.9) 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        color: #E8EAF6;
        border: 1px solid rgba(100, 255, 218, 0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(100, 255, 218, 0.2);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: #64FFDA; margin-bottom: 1rem;">🤖 DocuChat AI</h2>
        <p style="color: #B39DDB;">Intelligent Document Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Features")
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <strong>Multi-Format Support</strong><br>
        PDF, DOCX, TXT files
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <strong>AI-Powered</strong><br>
        Advanced question answering
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💭</div>
        <strong>Memory Feature</strong><br>
        Remembers conversation context
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <strong>Fast & Accurate</strong><br>
        Instant responses with sources
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("• Upload your document first\n• Ask follow-up questions\n• Memory remembers context\n• Clear history when needed")
    
    # Clear conversation button
    if st.session_state.document_processed and st.session_state.qa_chain:
        if st.button("🗑️ Clear Conversation", help="Clear chat history and start fresh"):
            clear_memory(st.session_state.qa_chain)
            st.session_state.chat_history = []
            st.success("✅ Conversation cleared!")
            st.rerun()

# Main content
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🤖 DocuChat AI</h1>
        <p class="main-subtitle">Ask questions about your documents with AI-powered intelligence & memory</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown("### 📁 Upload Your Document")
    st.markdown("*Supported formats: PDF, DOCX, TXT*")
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx", "txt"],
        help="Upload a PDF, Word document, or text file to start asking questions"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question input section
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 🤔 Ask Your Question")
    question = st.text_input(
        "What would you like to know about your document?",
        placeholder="e.g., What is the main topic? Can you explain more about...?",
        help="Type your question here. The AI will remember previous questions for context!"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        # Process the uploaded file
        if not st.session_state.document_processed or st.session_state.qa_chain is None:
            with st.spinner("🔄 Processing your document..."):
                try:
                    if uploaded_file.type == "application/pdf":
                        text = load_pdf(uploaded_file)
                        file_type_icon = "📕"
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        text = load_docx(uploaded_file)
                        file_type_icon = "📘"
                    elif uploaded_file.type == "text/plain":
                        text = load_txt(uploaded_file)
                        file_type_icon = "📄"
                    else:
                        st.error("❌ Unsupported file type!")
                        st.stop()
                    
                    st.success(f"✅ {file_type_icon} Document processed successfully!")
                    
                    # Create vectorstore and QA chain with memory
                    vectorstore = create_vectorstore(text)
                    st.session_state.qa_chain = get_qa_chain_with_memory(vectorstore)
                    st.session_state.document_processed = True
                    
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
                    st.stop()

        # Chat History Display
        if st.session_state.chat_history:
            st.markdown('<div class="chat-history-card">', unsafe_allow_html=True)
            st.markdown("### 💭 Conversation History")
            
            for i, chat in enumerate(st.session_state.chat_history):
                st.markdown(f"""
                <div class="chat-message">
                    <div class="user-question">👤 Q{i+1}: {chat['question']}</div>
                    <div class="ai-answer">🤖 A{i+1}: {chat['answer']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Answer section
        if question and st.session_state.qa_chain:
            st.markdown('<div class="answer-card">', unsafe_allow_html=True)
            
            with st.spinner("🤖 AI is thinking with context..."):
                try:
                    # Use the conversational chain with memory
                    result = st.session_state.qa_chain({"question": question})
                    
                    st.markdown("### ✨ AI Answer")
                    st.markdown(f"**Q:** {question}")
                    st.markdown(f"**A:** {result['answer']}")
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": result['answer']
                    })
                    
                    # Sources section
                    if "source_documents" in result and result["source_documents"]:
                        with st.expander("📚 View Sources & Context", expanded=False):
                            for i, doc in enumerate(result["source_documents"], 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(f"```\n{doc.page_content[:400]}{'...' if len(doc.page_content) > 400 else ''}\n```")
                                st.markdown("---")
                    
                    # Show memory indicator
                    memory_count = len(st.session_state.chat_history)
                    if memory_count > 1:
                        st.info(f"💭 **Contextual Memory Active** - Remembering {memory_count} previous exchanges")
                    
                except Exception as e:
                    st.error(f"❌ Error generating answer: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif question:
        st.warning("⚠️ Please upload a document first to ask questions!")

