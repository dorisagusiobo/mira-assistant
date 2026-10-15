# Mira Assistant

**A voice-first AI assistant you can talk to in the browser.**

Mira listens when you speak, answers out loud, and keeps your conversations so you can pick them back up later. An animated orb shows what she is doing: listening, thinking, speaking, or idle. You can also type.

## Features

- **Talk or type.** Speech recognition turns your voice into a message; speech synthesis reads Mira's reply aloud. A **Stop Voice** button cuts her off at any time.
- **Animated status orb.** The orb changes color and motion for each state (idle, listening, recognizing, thinking, speaking, error), so you always know what is happening without reading anything.
- **Saved conversations.** Every chat is stored in SQLite and listed in the sidebar. Click one to continue it; Mira receives the full history.
- **Works with OpenAI or OpenRouter.** Any OpenAI-compatible endpoint works through one setting.
- **Memory store.** A small key-value API for facts about the user, ready for personalization.

## Design decisions

- **Written to be heard.** Replies are plain spoken text with no Markdown, because symbols like `**` or tables are meaningless, or read out literally, when a reply is spoken.
- **Honest about limits.** Mira can only talk. She is instructed never to claim she set a reminder, checked a calendar, or took any action, and to suggest how you can do it yourself instead.
- **Failures don't corrupt the conversation.** Mira asks the AI first and saves your message and her reply together only when she gets an answer. If the AI is unavailable you see a clear message, and retrying never leaves duplicate or unanswered messages behind.
- **Calm without a key.** With no API key, Mira still runs and explains that she is in demo mode, so the interface can be tried right away.

## How it works

```
Browser (HTML, CSS, JavaScript)
  speech recognition --> message --+
                                   v
FastAPI backend --> chat service --> OpenAI-compatible LLM (OpenAI or OpenRouter)
       |                 |
       |                 +--> SQLite: sessions, messages, memory
       +--> serves the web app at /
                                   |
  speech synthesis <-- reply <-----+
```

| Layer | Technology |
|---|---|
| Frontend | Plain HTML, CSS and JavaScript; Web Speech API for voice in and out |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| AI | OpenAI Python SDK against OpenAI or OpenRouter |
| Data | SQLite |
| Tests | pytest (10 tests, AI faked so they cost nothing) |

## Run it locally

You need Python 3.11+ and an API key from [OpenAI](https://platform.openai.com/api-keys) or [OpenRouter](https://openrouter.ai/keys).

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env               # then add your key; see the file for OpenRouter
python run.py
```

Open http://127.0.0.1:8000. The backend serves the web app, so there is only one thing to run. API docs are at http://127.0.0.1:8000/docs.

Voice input needs a browser with the Web Speech API (Chrome or Edge). Typing works everywhere.

## Run the tests

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest -q
```

## API

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/chat` | Send a message; starts a session if none is given |
| `GET` | `/api/sessions` | List conversations, newest first |
| `GET` | `/api/sessions/{id}` | One conversation with its messages |
| `POST` / `GET` | `/api/memory` | Save or list key-value memories |
| `GET` | `/health` | Health check |

## Limitations

- Built for local, single-user use: there is no sign-in, so do not expose it to the internet as is.
- The memory store is not yet fed into conversations.

## Roadmap

- Use saved memories to personalize replies
- Stream replies so Mira starts speaking sooner
- Sign-in, so it can be hosted for more than one person

---

Built by **Doris Agusiobo Echianu**, AI engineer and designer. [Portfolio](https://doris-agusiobo-echianu.vercel.app) · [LinkedIn](https://www.linkedin.com/in/doris-agusiobo-echianu-83571764)
