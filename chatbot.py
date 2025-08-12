import os
from typing import List, Dict, Any
from openai import OpenAI
import logging
from vector_store import TFTVectorStore
import json

logger = logging.getLogger(__name__)

class TFTChatbot:
    """TFT Set 15 Q&A Chatbot"""
    
    def __init__(self, openai_api_key: str, vector_store: TFTVectorStore):
        self.client = OpenAI(api_key=openai_api_key)
        self.vector_store = vector_store
        self.conversation_history = []
        
        # System prompt for TFT-specific responses
        self.system_prompt = """You are a helpful assistant for Teamfight Tactics (TFT) Set 15. You have access to specific information about champions, traits, items, augments, and mechanics from TFT Set 15.

CRITICAL RULES:
1. ONLY use information that is explicitly provided in the context below
2. DO NOT use any general knowledge about TFT or League of Legends
3. DO NOT make assumptions or provide information that is not in the context
4. If the context doesn't contain enough information to answer a question, say "I don't have enough information about that in the knowledge base" or "The knowledge base doesn't contain details about that"
5. Be precise and accurate - only state facts that are directly supported by the provided context

SPECIAL HANDLING FOR LISTS:
- If you see summary documents like "Name: 5 1-cost champions", this indicates there are 5 champions of that tier
- You can list the individual champions you find in the context, but be clear about how many you found vs. how many should exist
- If you find fewer individual champions than the summary indicates, mention this
- DO NOT make up champion names or information that is not explicitly in the context

Your role is to:
1. Answer questions about TFT Set 15 champions and their tiers using ONLY the provided data
2. Explain traits and their effects ONLY if that information is in the context
3. Provide information about items and augments ONLY if that information is in the context
4. If asked about something not in the context, clearly state that the information is not available

Example responses:
- If asked about a champion's tier and it's in the context: "Aatrox is a Tier 1 champion"
- If asked about a trait effect and it's NOT in the context: "I don't have information about what the Bastion trait does in the knowledge base"
- If asked to list champions of a certain tier: List ONLY the champions you find in the context, and mention if there should be more based on summary documents
- If asked about trait effects and only the trait name is in context: "I can see that Bastion exists as a trait, but I don't have information about what it does in the knowledge base"

Keep responses concise and only include information that is directly supported by the provided context."""
    
    def get_response(self, user_message: str) -> str:
        """Get a response to the user's message"""
        try:
            # Enhanced search for tier-based queries
            context = self._get_enhanced_context(user_message)
            
            # Build messages array - start with system prompt
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history FIRST (if any)
            if self.conversation_history:
                messages.extend(self.conversation_history[-6:])  # Last 3 exchanges
            
            # Add current user message LAST
            messages.append({
                "role": "user", 
                "content": f"Context information:\n{context}\n\nUser question: {user_message}"
            })
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.1
            )
            
            assistant_response = response.choices[0].message.content
            
            # Update conversation history AFTER getting response
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return f"I apologize, but I encountered an error while processing your question. Please try again. Error: {str(e)}"
    
    def _get_enhanced_context(self, user_message: str) -> str:
        """Get enhanced context for tier-based queries"""
        message_lower = user_message.lower()

        # Check if this is a tier-based query
        tier_pattern = None

        # Robust parsing of tier number from message (supports "2 cost", "2-cost", "tier 2", "two cost", etc.)
        try:
            import re

            word_to_num = {
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
            }

            # Patterns capture numeric or word-based tier references
            regex_patterns = [
                r"\b([1-5])\s*-?\s*costs?\b",
                r"\bcosts?\s*-?\s*([1-5])\b",
                r"\btier\s*-?\s*([1-5])\b",
                r"\b(one|two|three|four|five)\s*-?\s*costs?\b",
                r"\btier\s*-?\s*(one|two|three|four|five)\b",
            ]

            detected_tier_number = None
            for pattern in regex_patterns:
                match = re.search(pattern, message_lower)
                if match:
                    value = match.group(1)
                    if value.isdigit():
                        detected_tier_number = int(value)
                    else:
                        detected_tier_number = word_to_num.get(value)
                    break

            if detected_tier_number in {1, 2, 3, 4, 5}:
                tier_pattern = f"Tier: {detected_tier_number}"
        except Exception:
            # Fall back to simple phrase checks if regex parsing fails for any reason
            if any(phrase in message_lower for phrase in ["1-cost", "tier 1", "cost 1", "1 cost"]):
                tier_pattern = "Tier: 1"
            elif any(phrase in message_lower for phrase in ["2-cost", "tier 2", "cost 2", "2 cost"]):
                tier_pattern = "Tier: 2"
            elif any(phrase in message_lower for phrase in ["3-cost", "tier 3", "cost 3", "3 cost"]):
                tier_pattern = "Tier: 3"
            elif any(phrase in message_lower for phrase in ["4-cost", "tier 4", "cost 4", "4 cost"]):
                tier_pattern = "Tier: 4"
            elif any(phrase in message_lower for phrase in ["5-cost", "tier 5", "cost 5", "5 cost"]):
                tier_pattern = "Tier: 5"
        
        if tier_pattern:
            # For tier-based queries, use pattern search to find ALL champions of that tier
            try:
                matching_docs = self.vector_store.search_by_pattern(tier_pattern)
                
                # Filter to only include champion documents (not summary documents)
                champion_docs = []
                for doc in matching_docs:
                    content = doc.get('content', '')
                    if 'Name:' in content and tier_pattern in content and 'champions' not in content.lower():
                        champion_docs.append(doc)
                
                # Create context from all matching champion documents
                context = f"Found {len(champion_docs)} {tier_pattern} champions:\n\n"
                for i, doc in enumerate(champion_docs, 1):
                    context += f"Document {i}:\n{doc['content']}\n\n"
                
                return context.strip()
                
            except Exception as e:
                logger.error(f"Error in pattern search: {e}")
                # Fallback to vector search
                return self.vector_store.get_relevant_context(tier_pattern, k=20)
        else:
            # For non-tier queries, use the original approach
            return self.vector_store.get_relevant_context(user_message, k=20)
    
    def get_suggested_questions(self) -> List[str]:
        """Get a list of suggested questions for the user"""
        return [
            "What does the Luchador trait do?",
            "Tell me about the Mighty Mech trait",
            "What are the best items for carries?",
            "How do power-ups work in Set 15?",
            "What champions synergize with Luchador?",
            "Explain the Doublestrike power-up",
            "What items should I build on tanks?",
            "What augments are available for Battle Academia?",
            "How do region portals work?",
            "What tier is Aatrox in Set 15?"
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
                logger.info("Building new index with placeholder data...")
                
                # Temporary placeholder data until better source is found
                documents = self.create_placeholder_documents()
                
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
    
    def create_placeholder_documents(self):
        """Create comprehensive TFT Set 15 documents from the knowledge base"""
        try:
            # Load the main TFT15 knowledge base
            knowledge_base_path = "tft15_knowledge_base.json"
            if os.path.exists(knowledge_base_path):
                with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                    knowledge_base = json.load(f)
                
                documents = knowledge_base.get("documents", [])
                logger.info(f"Loaded {len(documents)} documents from TFT15 knowledge base")
                return documents
            
            # Fallback to enhanced knowledge base if main one doesn't exist
            enhanced_kb_path = "tft15_enhanced_knowledge_base.json"
            if os.path.exists(enhanced_kb_path):
                with open(enhanced_kb_path, 'r', encoding='utf-8') as f:
                    knowledge_base = json.load(f)
                
                documents = knowledge_base.get("documents", [])
                logger.info(f"Loaded {len(documents)} documents from enhanced TFT15 knowledge base")
                return documents
            else:
                logger.warning(f"Knowledge base files not found, using fallback data")
                return self.create_fallback_documents()
            
        except Exception as e:
            logger.error(f"Error loading TFT15 knowledge base: {e}")
            return self.create_fallback_documents()
    
    def create_fallback_documents(self):
        """Create fallback documents if knowledge base is not available"""
        return [
            {
                'content': 'TFT Set 15 is the latest set of Teamfight Tactics. The knowledge base file was not found, so this is fallback information.',
                'metadata': {
                    'type': 'fallback',
                    'source': 'fallback_data',
                    'note': 'Knowledge base file not found'
                }
            }
        ]
    
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