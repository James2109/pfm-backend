# PFM Backend

REST API backend for **Personal Football Manager** — an app for managing players, training plans, and an AI football coach.

## Tech Stack

- **FastAPI** — Python web framework
- **Supabase** — Database & Auth (PostgreSQL)
- **LangGraph + LangChain** — AI agent pipeline
- **Google Gemini** — LLM (chat & plan generation)
- **uv** — Package manager

## Project Structure

```
src/
├── api/v1/routes/       # Endpoints: users, players, conversations, messages, plans
├── core/                # Config, security, dependencies, lifespan
├── models/              # Pydantic models
├── repositories/        # Database queries (Supabase)
├── services/            # Business logic (chat, agent, llm)
├── prompts/             # YAML prompt templates
└── main.py              # App entry point
```

## Requirements

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/)
- Supabase account
- Google Gemini API key

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd pfm-backend

# Install dependencies
uv sync

# Create .env file
cp .env.example .env
```

## Environment Variables

Create a `.env` file with the following:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_gemini_api_key
HEADER_AUTH_KEY=your_api_key
```

## Running the Server

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/me` | Get current user info |
| PATCH | `/api/v1/users/me` | Update current user info |
| GET | `/api/v1/players/` | List all players |
| POST | `/api/v1/players/` | Create a player |
| GET | `/api/v1/conversations/user/{id}` | Get conversations by user |
| POST | `/api/v1/conversations/chat` | Send message to AI coach |
| PATCH | `/api/v1/conversations/{id}` | Rename a conversation |
| DELETE | `/api/v1/conversations/{id}` | Delete a conversation |
| GET | `/api/v1/plans/user/{id}` | Get plans by user |
| POST | `/api/v1/plans/generate` | Generate training/nutrition plan with AI |

> All requests require the `X-API-Key: <HEADER_AUTH_KEY>` header and a Bearer token (Supabase JWT).
