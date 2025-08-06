from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your existing chatbot
from chatbot import TFTChatbotManager

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize chatbot manager
chatbot_manager = None

def initialize_chatbot():
    global chatbot_manager
    try:
        # Get OpenAI API key from environment
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            print("Please make sure your .env file contains: OPENAI_API_KEY=your_api_key_here")
            return False
        
        print("🔧 Initializing TFTChatbotManager...")
        print("🚀 VERSION: Enhanced Search Enabled (v2.0)")
        chatbot_manager = TFTChatbotManager(openai_api_key)
        
        # Initialize the chatbot (this will load/create the vector store)
        print("🔧 Initializing vector store...")
        chatbot_manager.initialize(force_rebuild=False)
        
        # Verify enhanced search is available
        if hasattr(chatbot_manager.chatbot, '_get_enhanced_context'):
            print("✅ Enhanced search functionality: AVAILABLE")
        else:
            print("❌ Enhanced search functionality: MISSING")
            return False
        
        print("✅ Chatbot initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not chatbot_manager:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        # Get response from your existing chatbot
        response = chatbot_manager.get_response(message)
        
        # Add cache-busting headers to prevent browser caching
        response_obj = jsonify({'response': response})
        response_obj.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response_obj.headers['Pragma'] = 'no-cache'
        response_obj.headers['Expires'] = '0'
        
        return response_obj
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'chatbot_initialized': chatbot_manager is not None
    })

@app.route('/api/knowledge-base-info', methods=['GET'])
def knowledge_base_info():
    try:
        # Load the main TFT15 knowledge base
        kb_file = 'tft15_knowledge_base.json'
        if not os.path.exists(kb_file):
            kb_file = 'tft15_enhanced_knowledge_base.json'
        
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
        
        documents = kb_data.get('documents', [])
        
        return jsonify({
            'knowledge_base_file': kb_file,
            'total_documents': len(documents),
            'document_types': {
                'champions': len([doc for doc in documents if doc.get('metadata', {}).get('type') == 'champion']),
                'traits': len([doc for doc in documents if doc.get('metadata', {}).get('type') == 'trait']),
                'items': len([doc for doc in documents if doc.get('metadata', {}).get('type') == 'item']),
                'power_ups': len([doc for doc in documents if doc.get('metadata', {}).get('type') == 'power_up']),
                'general': len([doc for doc in documents if doc.get('metadata', {}).get('type') == 'general'])
            }
        })
    except Exception as e:
        return jsonify({'error': f'Could not load knowledge base info: {e}'}), 500

@app.route('/api/test-enhanced-search', methods=['GET'])
def test_enhanced_search():
    """Test endpoint to verify enhanced search is working"""
    try:
        if not chatbot_manager:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        # Test the enhanced search functionality
        test_query = "List all 2-cost champions"
        context = chatbot_manager.chatbot._get_enhanced_context(test_query)
        
        # Check if it contains actual champion names
        has_champion_names = any(name in context.lower() for name in ['janna', 'jhin', 'kai', 'katarina'])
        
        return jsonify({
            'enhanced_search_available': hasattr(chatbot_manager.chatbot, '_get_enhanced_context'),
            'test_query': test_query,
            'context_preview': context[:200] + "..." if len(context) > 200 else context,
            'contains_champion_names': has_champion_names,
            'status': 'working' if has_champion_names else 'not_working'
        })
    except Exception as e:
        return jsonify({'error': f'Test failed: {e}'}), 500

if __name__ == '__main__':
    print("🚀 Starting TFT QA Bot Backend Server...")
    
    # Initialize chatbot
    if initialize_chatbot():
        print("🌐 Starting Flask server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize chatbot. Exiting.")
        sys.exit(1) 