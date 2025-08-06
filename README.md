# TFT Set 15 Q&A Chatbot

A comprehensive Q&A chatbot for Teamfight Tactics Set 15, helping players learn about champions, traits, items, and core mechanics. The chatbot provides accurate information based on official TFT Set 15 data without hallucination.

## Features

- **Champion Information**: Get detailed information about champion tiers, costs, and basic stats
- **Trait Database**: Access information about traits and their effects
- **Item Database**: Search for items and their effects
- **Augment Information**: Learn about augments and their benefits
- **Enhanced Search**: Find all champions of any specific cost tier
- **Interactive Chat Interface**: Modern React-based chat interface
- **No Hallucination**: Only provides information that exists in the knowledge base

## Tech Stack

- **Backend**: Python Flask API
- **Frontend**: React/Next.js with TypeScript
- **Data Source**: Official TFT Set 15 JSON data files
- **Embeddings**: OpenAI text-embedding-ada-002
- **Vector Store**: FAISS for efficient similarity search
- **LLM**: OpenAI GPT-3.5-turbo
- **Styling**: Tailwind CSS

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

### 6. Install Frontend Dependencies
```bash
npm install
```

### 7. Run the Application

**Start the Backend Server:**
```bash
python backend_server.py
```

**Start the Frontend (in a new terminal):**
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Project Structure

```
tft-qa-bot/
├── backend_server.py      # Flask API server
├── chatbot.py            # Chatbot logic and prompts
├── vector_store.py       # FAISS vector store operations
├── requirements.txt      # Python dependencies
├── src/                  # React frontend source code
│   ├── app/             # Next.js app directory
│   ├── components/      # React components
│   └── lib/            # Utility libraries
├── package.json         # Node.js dependencies
├── tft15_knowledge_base.json  # TFT Set 15 data
├── tft-*.json          # Raw TFT data files
├── .env                # Environment variables (create this)
└── README.md          # This file
```

## Usage

1. Start both the backend server and frontend application
2. Open your browser to http://localhost:3000
3. Ask questions about TFT Set 15 champions, traits, items, or mechanics
4. Get instant, accurate answers based on official game data

## Example Questions

- "List all 1-cost champions"
- "What tier is Aatrox?"
- "What does the Bastion trait do?"
- "Tell me about the Bastion Emblem item"
- "What does the Bastion Crest augment do?"
- "List all 5-cost champions"

## API Endpoints

- `GET /api/health` - Check server health
- `GET /api/knowledge-base-info` - Get information about the knowledge base
- `POST /api/chat` - Send a message to the chatbot

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details 