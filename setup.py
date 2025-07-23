#!/usr/bin/env python3
"""
Setup script for TFT Set 15 Q&A Bot
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    print("📁 Creating virtual environment...")
    try:
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    # Determine the pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if env_file.exists():
        print("📄 .env file already exists")
        return True
    
    print("📄 Creating .env file...")
    try:
        with open(env_file, 'w') as f:
            f.write("# OpenAI API Key\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("\n# Add your OpenAI API key above\n")
            f.write("# Get one at: https://platform.openai.com/api-keys\n")
        
        print("✅ .env file created")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test Python imports
    test_script = """
import sys
sys.path.insert(0, '.')

try:
    import streamlit
    import openai
    import faiss
    import langchain
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
"""
    
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} -c \"{test_script}\"", "Testing imports")

def main():
    """Main setup function"""
    print("🚀 Setting up TFT Set 15 Q&A Bot...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Get an API key from: https://platform.openai.com/api-keys")
    print("3. Run the application:")
    print("   - Windows: venv\\Scripts\\streamlit run app.py")
    print("   - Unix/Linux/macOS: venv/bin/streamlit run app.py")
    print("\n🐳 Or use Docker:")
    print("   docker-compose up --build")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 