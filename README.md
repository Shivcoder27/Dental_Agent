# Dental AI Agent

A dental clinic assistant stack: a **FastAPI** backend for patients and appointments, a **Telegram bot** for natural-language interactions, **RAG** (FAISS + sentence transformers) for patient context, **OpenRouter** for LLM calls, **SQLAlchemy** persistence, and **Twilio** SMS for confirmations and reminders (via APScheduler).

## Features

- **REST API**: Create, list, read, update, and delete patients; schedule appointments.
- **Telegram bot**: Greetings, patient CRUD via intent parsing, appointment scheduling from free text.
- **Vector store**: Patient records are indexed at startup and when new patients are created via the bot.
- **Reminders**: Background job every 10 minutes sends SMS reminders (window around 5 hours before appointment time, as implemented in the scheduler).

## Requirements

- Python 3.10+ (recommended)
- A SQL database supported by SQLAlchemy (PostgreSQL or MySQL URLs work with the listed drivers)
- [OpenRouter](https://openrouter.ai/) API key for chat completions
- Optional: [Telegram Bot](https://core.telegram.org/bots/tutorial) token
- Optional: [Twilio](https://www.twilio.com/) account for SMS (confirmation + reminders)

## Installation

From the `Dental_Agent` directory:

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install twilio
```

**macOS / Linux:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
pip install twilio
```

> **Note:** `twilio` is used by `app/services/sms_service.py` but is not listed in `requirements.txt`; install it explicitly until it is added to the file.

## Environment variables

Create a `.env` file in `Dental_Agent` (same folder as `run_server.py`):

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | SQLAlchemy URL, e.g. `postgresql+psycopg2://user:pass@localhost:5432/dental` or `mysql+pymysql://user:pass@localhost:3306/dental` |
| `OPEN_ROUTE_API_KEY` | OpenRouter API key (used in `app/integrations/gemini_client.py`) |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather |
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `TWILIO_AUTH_TOKEN` | Twilio auth token |
| `TWILIO_PHONE_NUMBER` | Twilio sender number (E.164) |

## Running the application

The bot calls the API at `http://127.0.0.1:8000`. Start the API first, then the bot (in two terminals).

**1. API server**

```bash
cd Dental_Agent
python run_server.py
```

Or:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Root:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) — health JSON  
- **OpenAPI docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**2. Telegram bot** (optional)

```bash
cd Dental_Agent
python -m app.bot.run_bot
```

On startup, the API creates database tables, loads existing patients into the vector index, and starts the reminder scheduler.

## API overview

### Patients (`/patients`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/patients/` | Create patient (body: `name`, `phone`, `age`, `gender`) |
| `GET` | `/patients/` | List all patients |
| `GET` | `/patients/{patient_id}` | Get one patient |
| `PUT` | `/patients/{patient_id}` | Update patient |
| `DELETE` | `/patients/{patient_id}` | Delete patient |

### Appointments (`/appointments`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/appointments/` | Schedule appointment (body: `patient_id`, `treatment`, `appointment_time` ISO datetime) |

Successful scheduling triggers a confirmation SMS via Twilio when configured.

## Project layout

```
Dental_Agent/
├── run_server.py              # Uvicorn entry (FastAPI)
├── requirements.txt
├── app/
│   ├── main.py                # App factory, startup, routers
│   ├── api/                   # FastAPI routers
│   ├── agents/                # Intent + appointment parsing (LLM)
│   ├── bot/                   # Telegram handlers
│   ├── database/              # Models, engine, repositories
│   ├── integrations/          # OpenRouter client
│   ├── rag/                   # FAISS vector store + retriever
│   ├── scheduler/             # APScheduler reminder job
│   ├── schemas/               # Pydantic models
│   ├── services/              # Business logic, SMS, AI
│   └── utils/                 # Conversation memory (bot)
└── tests/
    └── test_sms.py
```

## Tests

```bash
cd Dental_Agent
pytest
```

## Troubleshooting

- **Bot cannot create patients / appointments:** Ensure the API is running on port `8000` before starting the bot (the bot uses fixed `http://127.0.0.1:8000` URLs).
- **Database errors:** Verify `DATABASE_URL` and that the database exists; drivers must match the URL scheme (`psycopg2` / `pymysql`).
- **LLM / intent errors:** Check `OPEN_ROUTE_API_KEY` and OpenRouter account limits; intent parsing expects strict JSON from the model.
- **SMS not sending:** Confirm Twilio credentials and that patient phone numbers are valid for your Twilio region (India `+91` prefix is applied in code for outbound SMS).


