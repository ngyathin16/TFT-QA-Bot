# TFT Set 15 Q&A Chatbot

A comprehensive Q&A chatbot for Teamfight Tactics Set 15, helping players learn about champions, traits, items, and core mechanics. The chatbot provides accurate information based on official TFT Set 15 data without hallucination.

## Live demo

- Frontend: [tft-qa-bot.vercel.app](https://tft-qa-bot.vercel.app)
- Backend health: [`https://<your-render-backend>/api/health`](https://<your-render-backend>/api/health)
- Enhanced search test: [`https://<your-render-backend>/api/test-enhanced-search`](https://<your-render-backend>/api/test-enhanced-search)

Note: The frontend relies on the backend. If you fork this repo, set the Vercel env var `BACKEND_URL` to your Render backend URL.

## Features

- **Champion Information**: Get detailed information about champion tiers, costs, and basic stats
- **Trait Database**: Access information about traits and their effects
- **Item Database**: Search for items and their effects
- **Augment Information**: Learn about augments and their benefits
- **Enhanced Tier Search (Robust Parsing)**: Accurately finds all champions of a specific cost tier. Supports phrasing such as "2-cost", "2 cost", "tier 2", and "tier two"
- **Interactive Chat Interface**: Modern React-based chat interface
- **No Hallucination**: Only provides information that exists in the knowledge base
- **Operational Diagnostics**: Health and verification endpoints to confirm correct knowledge base loading and enhanced search behavior

## Tech Stack

- **Backend**: Python Flask API
- **Frontend**: React/Next.js with TypeScript
- **Data Source**: Official TFT Set 15 JSON data files
- **Embeddings**: OpenAI text-embedding-ada-002
- **Vector Store**: FAISS for efficient similarity search
- **LLM**: OpenAI GPT-3.5-turbo
- **Styling**: Tailwind CSS

## Architecture overview

The app is split into a statically hosted frontend and a Python backend:

- **Frontend (Next.js on Vercel)**
  - User requests are sent to `src/app/api/chat/route.ts`, which forwards the message to the backend at `BACKEND_URL`
  - A cache-busting timestamp is added to avoid any intermediary caching

- **Backend (Flask on Render)**
  - `backend_server.py` exposes `/api/chat`, `/api/health`, `/api/knowledge-base-info`, and `/api/test-enhanced-search`
  - `chatbot.py` orchestrates the LLM and the vector store, and implements the enhanced tier search
  - `vector_store.py` manages embeddings, FAISS index creation/loading, and searches

- **Knowledge base**
  - Primary file: `tft15_knowledge_base.json` with `documents` containing champion/trait/item entries
  - Champion entries use a compact format, for example: `Name: Aatrox\nTier: 1`
  - The backend builds or loads a FAISS index from these documents (`tft15_index.faiss` + `tft15_index.pkl`)

## Quick Start (Recommended)

### Option 1: Automatic Setup (Windows)
```powershell
# Clone the repository
git clone https://github.com/ngyathin16/TFT-QA-Bot.git
cd TFT-QA-Bot

# Run the complete fix script (handles everything)
.\FINAL_FIX.ps1
```

### Option 2: Manual Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/ngyathin16/TFT-QA-Bot.git
cd TFT-QA-Bot
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
npm install
```

#### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

#### 5. Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

#### 6. Run the Application

**Start the Backend Server:**
```bash
PORT=5000 python backend_server.py
```

**Start the Frontend (in a new terminal):**
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## How the chatbot answers accurately

1. The frontend forwards your message to the backend.
2. The backend extracts relevant context from the FAISS index:
   - For general questions, it uses vector similarity search
   - For tier questions, it uses the enhanced tier search which now robustly detects phrasing like "2 cost", "tier two", etc.
3. The system prompt instructs the model to only answer from the provided context and avoid hallucinations.

## Deployment (Free Tier)

- **Frontend (Vercel)**: Deploy to Vercel. Set `BACKEND_URL` environment variable to your backend URL. Changes to frontend code or `BACKEND_URL` require a redeploy.
- **Backend (Render)**: Deploy to Render (Free Web Service). Add env var `OPENAI_API_KEY`, ensure `Start Command` is `python backend_server.py`. Render sets `PORT` automatically. Backend pushes to the tracked branch trigger auto-deploys.

### Post-deploy verification checklist

1. Open `https://<your-backend>/api/health` → should return `{ status: "healthy", chatbot_initialized: true }`
2. Open `https://<your-backend>/api/knowledge-base-info` → verify the knowledge base file and document counts are non-zero
3. Open `https://<your-backend>/api/test-enhanced-search` → `status` should be `working`, and `context_preview` should include real 2‑cost champion names
4. Visit the Vercel app and hard refresh, then ask: "List all the 2 cost champions" or "List all tier two champions"

Note: For backend-only code changes, you generally do not need to redeploy Vercel. Render will auto-redeploy the backend.

## Project Structure

```
TFT-QA-Bot/
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
├── FINAL_FIX.ps1       # Complete fix script
├── verify_fix.ps1      # Verification script
├── TROUBLESHOOTING.md  # Troubleshooting guide
└── README.md          # This file
```

## Usage

1. Start both the backend server and frontend application
2. Open your browser to http://localhost:3000
3. Press `Ctrl+Shift+R` for a hard refresh to clear any cached data
4. Ask questions about TFT Set 15 champions, traits, items, or mechanics
5. Get instant, accurate answers based on official game data

## Troubleshooting

If you encounter issues with the chatbot returning generic responses instead of specific champion names:

1. **Run the complete fix script:**
   ```powershell
   .\FINAL_FIX.ps1
   ```

2. **Verify the fix:**
   ```powershell
   .\verify_fix.ps1
   ```

3. **Check the troubleshooting guide:**
   - See `TROUBLESHOOTING.md` for detailed solutions

### Diagnostics and common causes

- Hit the diagnostic endpoints:
  - `GET /api/health` confirms the backend is up and the chatbot is initialized
  - `GET /api/knowledge-base-info` confirms the knowledge base file is present and parsed
  - `GET /api/test-enhanced-search` verifies the enhanced tier search is functioning

- Common deployment pitfalls:
  - Missing `OPENAI_API_KEY` on Render → embeddings and searches fail
  - `BACKEND_URL` missing on Vercel → frontend calls localhost instead of the deployed backend
  - Stale build on Render → click "Clear build cache & deploy" to force a clean build
  - Browser caching → perform a hard refresh on the frontend

## Available Scripts

- `FINAL_FIX.ps1` - Complete environment reset and restart
- `verify_fix.ps1` - Test if the chatbot is working correctly
- `fix_chatbot.ps1` - Alternative complete fix
- `force_restart.ps1` - Aggressive restart (if needed)

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
- `GET /api/test-enhanced-search` - Verifies the enhanced tier search is working and previews the context used

### `/api/chat`

Request body:

```json
{ "message": "List all the 2 cost champions" }
```

Response body:

```json
{ "response": "Janna, Jhin, Kai'Sa, Katarina, ..." }
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details 
