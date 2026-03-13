# Football Manager API Documentation

## Overview

A FastAPI-powered backend for managing football players, AI-powered coaching conversations, and personalized training/nutrition plan generation.

- **Base URL**: `/api/v1`
- **Framework**: FastAPI (async)
- **Database**: Supabase (PostgreSQL)
- **AI Engine**: Google Gemini + LangGraph

---

## Authentication

All endpoints require the `X-API-Key` header. Protected endpoints additionally require a JWT token.

| Header | Required | Description |
|--------|----------|-------------|
| `X-API-Key` | All endpoints | API key for service authentication |
| `Authorization` | Protected endpoints | `Bearer <jwt_token>` from Supabase Auth |

---

## Enums

### Position
```
Goalkeeper, Center Back, Left Back, Right Back, Wing Back, Sweeper,
Defensive Midfielder, Center Midfielder, Attacking Midfielder,
Left Midfielder, Right Midfielder, Striker, Center Forward,
Left Winger, Right Winger, Second Striker
```

### League
```
Premier League, Bundesliga, Serie A, La Liga, Ligue 1
```

### Frequency
```
daily, weekly, monthly, yearly
```

### Evaluation (Star Rating)
```
1, 2, 3, 4, 5
```

### MessageFrom
```
bot, human
```

---

## Endpoints

### Users

All endpoints require JWT authentication.

#### `GET /api/v1/users/me`

Get the current authenticated user profile.

**Response** `200 OK`
```json
{
  "id": "uuid",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### `PATCH /api/v1/users/me`

Update the current user profile.

**Request Body**
```json
{
  "first_name": "John",        // optional
  "last_name": "Doe",          // optional
  "full_name": "John Doe",     // optional
  "phone_number": "+1234567890" // optional
}
```

**Response** `200 OK` — Updated User object

#### `DELETE /api/v1/users/me`

Delete the current user account.

**Response** `204 No Content`

---

### Conversations

All endpoints require JWT authentication.

#### `GET /api/v1/conversations/`

List all conversations.

**Response** `200 OK` — Array of Conversation objects

#### `GET /api/v1/conversations/{conversation_id}`

Get a specific conversation.

**Response** `200 OK`
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Training advice for strikers",
  "message_count": 4,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### `GET /api/v1/conversations/user/{user_id}`

List all conversations for a specific user.

**Response** `200 OK` — Array of Conversation objects

#### `POST /api/v1/conversations/`

Create a new conversation.

**Request Body**
```json
{
  "user_id": "uuid",
  "title": "My conversation"
}
```

**Response** `201 Created` — Conversation object

#### `POST /api/v1/conversations/chat`

Send a message and receive an AI response. If `conversation_id` is omitted, a new conversation is automatically created.

**Request Body**
```json
{
  "message": "How can I improve my dribbling?",
  "conversation_id": "uuid"  // optional — auto-creates if null
}
```

**Response** `200 OK`
```json
{
  "conversation_id": "uuid",
  "user_message": {
    "id": "uuid",
    "conversation_id": "uuid",
    "message_from": "human",
    "message": "How can I improve my dribbling?",
    "reason": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  },
  "bot_message": {
    "id": "uuid",
    "conversation_id": "uuid",
    "message_from": "bot",
    "message": "Here are some tips to improve your dribbling...",
    "reason": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
}
```

#### `DELETE /api/v1/conversations/{conversation_id}`

Delete a conversation.

**Response** `204 No Content`

---

### Messages

All endpoints require JWT authentication.

#### `GET /api/v1/messages/`

List all messages.

**Response** `200 OK` — Array of Message objects

#### `GET /api/v1/messages/{message_id}`

Get a specific message.

**Response** `200 OK`
```json
{
  "id": "uuid",
  "conversation_id": "uuid",
  "message_from": "bot",
  "message": "Here is your answer...",
  "reason": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### `GET /api/v1/messages/conversation/{conversation_id}`

List all messages in a conversation.

**Response** `200 OK` — Array of Message objects (ordered by created_at)

#### `POST /api/v1/messages/`

Create a new message.

**Request Body**
```json
{
  "conversation_id": "uuid",
  "message_from": "human",
  "message": "Hello",
  "reason": null  // optional
}
```

**Response** `201 Created` — Message object

#### `DELETE /api/v1/messages/{message_id}`

Delete a message.

**Response** `204 No Content`

---

### Plans

All endpoints require JWT authentication.

#### `GET /api/v1/plans/`

List all plans.

**Response** `200 OK` — Array of Plan objects

#### `GET /api/v1/plans/{plan_id}`

Get a specific plan.

**Response** `200 OK`
```json
{
  "id": "uuid",
  "plan_name": "Striker Development Plan",
  "user_id": "uuid",
  "age": 22,
  "position": "Striker",
  "height": 180.0,
  "weight": 75.0,
  "strength": "Fast pace, strong header",
  "weakness": "Weak left foot",
  "note": "Recovering from ankle injury",
  "frequency": "weekly",
  "training_sessions": 4,
  "cost_per_meal": 15.0,
  "nutrition_plan": "## Nutrition Plan\n...",
  "training_plan": "## Training Plan\n...",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### `GET /api/v1/plans/user/{user_id}`

List all plans for a specific user.

**Response** `200 OK` — Array of Plan objects

#### `POST /api/v1/plans/`

Save a plan (typically after generating with AI).

**Request Body**
```json
{
  "plan_name": "Striker Development Plan",
  "user_id": "uuid",
  "age": 22,
  "position": "Striker",
  "height": 180.0,
  "weight": 75.0,
  "strength": "Fast pace, strong header",
  "weakness": "Weak left foot",
  "note": "Recovering from ankle injury",
  "frequency": "weekly",
  "training_sessions": 4,
  "cost_per_meal": 15.0,
  "nutrition_plan": "## Nutrition Plan\n...",
  "training_plan": "## Training Plan\n...",
  "reason": "This plan targets striker-specific skills..."
}
```

**Response** `201 Created` — Plan object

#### `POST /api/v1/plans/generate`

Generate a personalized training & nutrition plan using AI (Gemini).

**Request Body**
```json
{
  "age": 22,
  "position": "Striker",
  "height": 180.0,
  "weight": 75.0,
  "strength": "Fast pace, strong header",
  "weakness": "Weak left foot",
  "note": "Recovering from ankle injury",
  "frequency": "weekly",
  "training_sessions": 4,
  "cost_per_meal": 15.0
}
```

**Response** `200 OK`
```json
{
  "plan_name": "Striker Development Plan",
  "nutrition_plan": "## Weekly Nutrition Plan\n- **Breakfast**: ...",
  "training_plan": "## Weekly Training Schedule\n### Day 1: ...",
  "reason": "This plan is designed specifically for a striker..."
}
```

#### `DELETE /api/v1/plans/{plan_id}`

Delete a plan.

**Response** `204 No Content`

---

### Players

Players endpoints require only the `X-API-Key` header (no JWT).

#### `GET /api/v1/players/`

List all players.

**Response** `200 OK` — Array of Player objects

#### `GET /api/v1/players/{player_id}`

Get a specific player.

**Response** `200 OK`
```json
{
  "id": "uuid",
  "avatar_id": "avatar_001",
  "name": "Marcus Rashford",
  "age": 26,
  "nationality": "England",
  "league": "Premier League",
  "club": "Manchester United",
  "position": "Left Winger",
  "shirt_number": 10,
  "height": 180.0,
  "weight": 70.0,
  "right_foot": 4,
  "left_foot": 3,
  "skill": 4,
  "appearances": 250,
  "minutes_played": 18000,
  "goals": 75,
  "assists": 40,
  "clearances": 15,
  "yellow_cards": 20,
  "red_cards": 1,
  "max_speed": 35.5,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### `GET /api/v1/players/search/{name}`

Search players by name.

**Response** `200 OK` — Array of matching Player objects

#### `POST /api/v1/players/`

Create a new player.

**Request Body** — All Player fields except `id`, `created_at`, `updated_at`

**Response** `201 Created` — Player object

#### `PATCH /api/v1/players/{player_id}`

Update a player. All fields are optional.

**Request Body** — Partial Player fields

**Response** `200 OK` — Updated Player object

#### `DELETE /api/v1/players/{player_id}`

Delete a player.

**Response** `204 No Content`

---

## Architecture

```
src/
├── api/v1/
│   ├── router.py              # Main API router
│   └── routes/                # Endpoint handlers
│       ├── users.py
│       ├── conversations.py
│       ├── messages.py
│       ├── plans.py
│       └── players.py
├── core/
│   ├── config.py              # Settings (env vars)
│   ├── security.py            # Password hashing & JWT
│   ├── dependencies.py        # Dependency injection
│   ├── lifespan.py            # App startup/shutdown
│   └── log.py                 # System logger
├── models/                    # Pydantic schemas
├── repositories/              # Database operations (Supabase)
├── services/
│   ├── llm_service.py         # Gemini AI for plan generation
│   ├── chat_service.py        # Chat orchestration
│   └── agent_service.py       # LangGraph agent
├── prompts/                   # YAML prompt templates
│   ├── llm_prompt.yaml
│   └── agent_prompt.yaml
└── main.py                    # FastAPI app entry point
```

### Key Flows

**Chat Flow**: User message → ChatService → saves to DB → AgentService (LangGraph + Gemini) → saves bot response → returns both messages

**Plan Generation Flow**: Player profile input → GeminiService → structured JSON response (plan name, training plan, nutrition plan, reason) → returned to client for review/save

### Database Tables

| Table | Description |
|-------|-------------|
| `users` | User profiles (synced with Supabase Auth) |
| `conversations` | Chat conversation metadata |
| `messages` | Individual messages within conversations |
| `plans` | Saved training & nutrition plans |
| `players` | Football player profiles and statistics |
| `system_logs` | Application logs (level, component, message) |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase API key |
| `GEMINI_API_KEY` | Google Gemini API key |
| `HEADER_AUTH_KEY` | API key for X-API-Key header validation |
