import os
from typing import List, Dict, Any
from openai import OpenAI
import logging
from vector_store import TFTVectorStore

logger = logging.getLogger(__name__)

class TFTChatbot:
    """TFT Set 15 Q&A Chatbot"""
    
    def __init__(self, openai_api_key: str, vector_store: TFTVectorStore):
        self.client = OpenAI(api_key=openai_api_key)
        self.vector_store = vector_store
        self.conversation_history = []
        
        # System prompt for TFT-specific responses
        self.system_prompt = """You are a helpful assistant for Teamfight Tactics (TFT) Set 15. You have access to detailed information about champions, traits, items, and mechanics from the latest set.

Your role is to:
1. Answer questions about TFT Set 15 champions, their abilities, and synergies
2. Explain traits and their effects
3. Provide information about items and their stats
4. Help with game mechanics and strategies
5. Be accurate and informative while being friendly and helpful

Always base your answers on the provided context from the TFT Set 15 data. If you don't have enough information to answer a question accurately, say so rather than making up information.

Keep responses concise but informative, and feel free to use TFT terminology that players would understand."""
    
    def get_response(self, user_message: str) -> str:
        """Get a response to the user's message"""
        try:
            # Get relevant context from vector store
            context = self.vector_store.get_relevant_context(user_message, k=3)
            
            # Build the conversation
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context information:\n{context}\n\nUser question: {user_message}"}
            ]
            
            # Add conversation history for context (last 5 exchanges)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Can be upgraded to gpt-4 for better responses
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return f"I apologize, but I encountered an error while processing your question. Please try again. Error: {str(e)}"
    
    def get_suggested_questions(self) -> List[str]:
        """Get a list of suggested questions for the user"""
        return [
            "What does the Luchador trait do?",
            "Which items give Lethality in Set 15?",
            "Tell me about the Mighty Mech trait",
            "What are the best items for carries?",
            "How does the Artistic KO mechanic work?",
            "What champions synergize with Luchador?",
            "Explain the Doublestrike mechanic",
            "What items should I build on tanks?"
        ]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get chatbot statistics"""
        return {
            "conversation_length": len(self.conversation_history),
            "vector_store_documents": len(self.vector_store.documents) if self.vector_store.documents else 0
        }

class TFTChatbotManager:
    """Manager class for handling chatbot initialization and operations"""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.vector_store = None
        self.chatbot = None
        
    def initialize(self, force_rebuild: bool = False):
        """Initialize the chatbot and vector store"""
        try:
            # Initialize vector store
            self.vector_store = TFTVectorStore(self.openai_api_key)
            
            # Check if index exists
            index_path = "tft15_index"
            if not force_rebuild and self.vector_store.index_exists(index_path):
                logger.info("Loading existing index...")
                self.vector_store.load_index(index_path)
            else:
                logger.info("Building new index...")
                from data_processor import TFTDataProcessor
                
                # Process data
                processor = TFTDataProcessor()
                documents = processor.create_documents()
                
                # Create embeddings and build index
                embeddings = self.vector_store.create_embeddings(documents)
                self.vector_store.build_index(documents, embeddings)
                
                # Save index
                self.vector_store.save_index(index_path)
            
            # Initialize chatbot
            self.chatbot = TFTChatbot(self.openai_api_key, self.vector_store)
            
            logger.info("Chatbot initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize chatbot: {e}")
            return False
    
    def get_response(self, message: str) -> str:
        """Get a response from the chatbot"""
        if not self.chatbot:
            return "Chatbot not initialized. Please try again."
        
        return self.chatbot.get_response(message)
    
    def get_suggestions(self) -> List[str]:
        """Get suggested questions"""
        if not self.chatbot:
            return []
        
        return self.chatbot.get_suggested_questions()
    
    def clear_history(self):
        """Clear conversation history"""
        if self.chatbot:
            self.chatbot.clear_history()

if __name__ == "__main__":
    # Test the chatbot
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY in your .env file")
        exit(1)
    
    # Initialize chatbot manager
    manager = TFTChatbotManager(api_key)
    if manager.initialize():
        # Test responses
        test_questions = [
            "What does the Luchador trait do?",
            "Tell me about items in Set 15"
        ]
        
        for question in test_questions:
            print(f"\nQ: {question}")
            response = manager.get_response(question)
            print(f"A: {response}")
    else:
        print("Failed to initialize chatbot") 