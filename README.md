# TFT Set 15 Q&A Chatbot

A comprehensive Q&A chatbot for Teamfight Tactics Set 15, helping players learn about champions, traits, items, and core mechanics.

## Features

- **Champion Information**: Get detailed information about champion abilities, stats, and synergies
- **Trait Explanations**: Understand how traits work and their effects
- **Item Database**: Search for items and their effects
- **Mechanic Guides**: Learn about Set 15's unique mechanics
- **Interactive Chat Interface**: Natural language Q&A powered by AI

## Tech Stack

- **Data Source**: Community Dragon API (TFT Set 15 data)
- **Embeddings**: OpenAI text-embedding-ada-002
- **Vector Store**: FAISS
- **LLM**: OpenAI GPT-4 (recommended) or GPT-3.5-turbo
- **Framework**: LangChain
- **UI**: Streamlit
- **Deployment**: Docker containerized

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd tft-qa-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

### 6. Run the Application
```bash
streamlit run app.py
```

## Project Structure

```
tft-qa-bot/
├── app.py                 # Main Streamlit application
├── data_processor.py      # Data scraping and processing
├── vector_store.py        # FAISS vector store operations
├── chatbot.py            # Chatbot logic and prompts
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## Usage

1. Start the application with `streamlit run app.py`
2. Open your browser to the provided URL (usually http://localhost:8501)
3. Ask questions about TFT Set 15 champions, traits, items, or mechanics
4. Get instant, accurate answers based on official game data

## Example Questions

- "What does the Reckoning trait do?"
- "Which items give Lethality in Set 15?"
- "Tell me about Champion X's ability"
- "What are the best items for Y champion?"
- "How does the new mechanic work?"

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details 