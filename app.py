import streamlit as st
import os
from dotenv import load_dotenv
import logging
from chatbot import TFTChatbotManager

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    st.error(f"Warning: Could not load .env file: {e}")
    st.info("Please make sure your .env file is properly formatted with UTF-8 encoding")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="TFT Set 15 Q&A Bot",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left-color: #2196F3;
    }
    .bot-message {
        background-color: #F3E5F5;
        border-left-color: #9C27B0;
    }
    .suggestion-button {
        margin: 0.25rem;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        border: 1px solid #ddd;
        background-color: #f8f9fa;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .suggestion-button:hover {
        background-color: #e9ecef;
        border-color: #adb5bd;
    }
    .stats-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the chatbot manager"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        st.stop()
    
    if "chatbot_manager" not in st.session_state:
        with st.spinner("Initializing TFT Q&A Bot..."):
            manager = TFTChatbotManager(api_key)
            if manager.initialize():
                st.session_state.chatbot_manager = manager
                st.success("✅ TFT Q&A Bot initialized successfully!")
            else:
                st.error("❌ Failed to initialize chatbot. Please check your API key and try again.")
                st.stop()

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🎮 TFT Set 15 Q&A Bot</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI assistant for Teamfight Tactics Set 15 knowledge")
    
    # Initialize chatbot
    initialize_chatbot()
    
    # Sidebar
    with st.sidebar:
        st.header("🤖 Bot Controls")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chatbot_manager.clear_history()
            st.session_state.messages = []
            st.rerun()
        
        # Force rebuild index
        if st.button("🔄 Rebuild Knowledge Base"):
            with st.spinner("Rebuilding knowledge base..."):
                api_key = os.getenv("OPENAI_API_KEY")
                manager = TFTChatbotManager(api_key)
                if manager.initialize(force_rebuild=True):
                    st.session_state.chatbot_manager = manager
                    st.success("✅ Knowledge base rebuilt successfully!")
                else:
                    st.error("❌ Failed to rebuild knowledge base.")
        
        # Stats
        st.header("📊 Statistics")
        if "chatbot_manager" in st.session_state:
            stats = st.session_state.chatbot_manager.chatbot.get_stats()
            st.metric("Conversation Length", stats["conversation_length"])
            st.metric("Knowledge Base Documents", stats["vector_store_documents"])
        
        # About section
        st.header("ℹ️ About")
        st.markdown("""
        This bot uses:
        - **Data Source**: Community Dragon API
        - **AI Model**: OpenAI GPT-3.5-turbo
        - **Vector Store**: FAISS
        - **Framework**: Streamlit
        
        Ask questions about TFT Set 15 champions, traits, items, and mechanics!
        """)
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about TFT Set 15..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    response = st.session_state.chatbot_manager.get_response(prompt)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.header("💡 Suggested Questions")
        
        if "chatbot_manager" in st.session_state:
            suggestions = st.session_state.chatbot_manager.get_suggestions()
            
            for suggestion in suggestions:
                if st.button(suggestion, key=f"sugg_{suggestion[:20]}"):
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    with st.chat_message("user"):
                        st.markdown(suggestion)
                    
                    # Get bot response
                    with st.chat_message("assistant"):
                        with st.spinner("🤔 Thinking..."):
                            response = st.session_state.chatbot_manager.get_response(suggestion)
                            st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        Made with ❤️ for TFT players | Data from Community Dragon API
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 