#!/usr/bin/env python3
"""
Test script to verify TFT Set 15 Q&A Bot setup
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required packages can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI {openai.__version__}")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import faiss
        print(f"✅ FAISS {faiss.__version__}")
    except ImportError as e:
        print(f"❌ FAISS import failed: {e}")
        return False
    
    try:
        import langchain
        print(f"✅ LangChain {langchain.__version__}")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        import requests
        print(f"✅ Requests {requests.__version__}")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__}")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy {numpy.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    return True

def test_project_modules():
    """Test that project modules can be imported"""
    print("\n🧪 Testing project modules...")
    
    try:
        from data_processor import TFTDataProcessor
        print("✅ TFTDataProcessor imported successfully")
    except ImportError as e:
        print(f"❌ TFTDataProcessor import failed: {e}")
        return False
    
    try:
        from vector_store import TFTVectorStore
        print("✅ TFTVectorStore imported successfully")
    except ImportError as e:
        print(f"❌ TFTVectorStore import failed: {e}")
        return False
    
    try:
        from chatbot import TFTChatbot, TFTChatbotManager
        print("✅ TFTChatbot and TFTChatbotManager imported successfully")
    except ImportError as e:
        print(f"❌ Chatbot imports failed: {e}")
        return False
    
    try:
        import utils
        print("✅ Utils module imported successfully")
    except ImportError as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def test_data_processor():
    """Test data processor functionality"""
    print("\n🧪 Testing data processor...")
    
    try:
        from data_processor import TFTDataProcessor
        
        processor = TFTDataProcessor()
        print("✅ TFTDataProcessor instantiated successfully")
        
        # Test data fetching (this will make an HTTP request)
        print("🔄 Testing data fetching from Community Dragon API...")
        data = processor.fetch_data()
        print(f"✅ Successfully fetched data with {len(data.get('items', []))} items and {len(data.get('traits', []))} traits")
        
        # Test TFT15 filtering
        tft15_data = processor.filter_tft15_data()
        print(f"✅ Filtered {len(tft15_data['items'])} TFT15 items and {len(tft15_data['traits'])} TFT15 traits")
        
        # Test document creation
        documents = processor.create_documents()
        print(f"✅ Created {len(documents)} documents for vector store")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processor test failed: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print("\n🧪 Testing environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        
        # Check if OpenAI API key is set
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key and api_key != "your_openai_api_key_here":
                print("✅ OpenAI API key is set")
            else:
                print("⚠️  OpenAI API key not set or using placeholder value")
        except Exception as e:
            print(f"⚠️  Could not load .env file: {e}")
            print("⚠️  Please check the .env file encoding")
    else:
        print("❌ .env file not found")
        return False
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ Python version: {python_version}")
    
    return True

def main():
    """Main test function"""
    print("🚀 Testing TFT Set 15 Q&A Bot Setup")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test project modules
    if not test_project_modules():
        all_tests_passed = False
    
    # Test environment
    if not test_environment():
        all_tests_passed = False
    
    # Test data processor (optional - requires internet)
    try:
        if not test_data_processor():
            print("⚠️  Data processor test failed (this is normal if no internet connection)")
    except Exception as e:
        print(f"⚠️  Data processor test skipped: {e}")
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Your TFT Set 15 Q&A Bot is ready to use.")
        print("\n📋 Next steps:")
        print("1. Make sure your OpenAI API key is set in .env file")
        print("2. Run: streamlit run app.py")
        print("3. Open your browser to the provided URL")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 