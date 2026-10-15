# Mira Assistant

Mira is a Sophia-style, voice-first AI assistant web app with a plain HTML/CSS/JavaScript frontend and a FastAPI backend.

## What is included

- Animated orb interface
- Voice input using browser speech recognition
- Voice output using browser speech synthesis
- Chat sessions stored in SQLite
- Memory endpoints for future personalization
- OpenAI-compatible backend integration
- Complete local development structure

## Project structure

```text
mira-assistant/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── prompts/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
└── README.md
```

## Full environment setup

### 1. Install prerequisites

Install these tools first:

- Python 3.11 or 3.12
- Git
- VS Code or Cursor
- Optional: Node.js LTS

Check installation:

```bash
python3 --version
git --version
node --version
```

### 2. Open the project in VS Code or Cursor

You can open the generated folder manually:

```bash
code /path/to/mira-assistant
```

Or in Cursor:

```bash
cursor /path/to/mira-assistant
```

### 3. Set up the backend virtual environment

```bash
cd mira-assistant/backend
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
cd mira-assistant/backend
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 5. Create your environment file

Copy the example file:

```bash
cp .env.example .env
```

Then edit `.env` and add your real API key:

```env
OPENAI_API_KEY=your_real_key_here
```

### 6. Start the backend

```bash
python run.py
```

API URLs:

- Backend root: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

### 7. Start the frontend

Open another terminal:

```bash
cd mira-assistant/frontend
python3 -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## How the backend works

### `config.py`
Loads environment variables like API keys, ports, database URL, and allowed CORS origins.

### `database.py`
Creates the SQLAlchemy engine and session factory.

### `models.py`
Defines three tables:

- `ChatSession`
- `ChatMessage`
- `UserMemory`

### `schemas.py`
Defines request and response models for FastAPI.

### `services/llm_service.py`
Loads the prompt files, connects to OpenAI, sends the conversation history, and returns Mira's response.

### `services/chat_service.py`
Handles the full chat flow:

1. creates a session if needed
2. stores the user message
3. pulls the conversation history
4. calls the LLM
5. stores the assistant reply
6. returns the response payload

### `routers/chat.py`
Exposes `POST /api/chat`.

### `routers/session.py`
Exposes:

- `GET /api/sessions`
- `GET /api/sessions/{session_id}`

### `routers/memory.py`
Exposes:

- `POST /api/memory`
- `GET /api/memory`

## How the frontend works

### `index.html`
Creates the full structure of the assistant UI:

- sidebar for chat sessions
- orb area
- transcript panel
- response panel
- voice controls
- text input composer

### `styles.css`
Defines the futuristic glassmorphism layout, glowing orb, state-based colors, responsive design, and chat session styling.

### `app.js`
Handles:

- backend API calls
- browser speech recognition
- browser speech synthesis
- session list rendering
- new chat flow
- orb state changes

## Notes for development

- If speech recognition is not available, use Chrome or Edge.
- If `OPENAI_API_KEY` is missing, the backend replies in demo mode.
- SQLite is used for local MVP development. You can swap to PostgreSQL later.

## Next recommended upgrades

- Streaming responses with WebSockets
- User authentication
- File uploads and summarization
- Task/reminder tools
- Calendar and email integrations
- Long-term memory extraction
- Mobile or desktop packaging
