# 🦷 Dental AI Agent

# Dental AI Agent

A dental clinic assistant stack: a **FastAPI** backend for patients and appointments, a **Telegram bot** for natural-language interactions, **RAG** (FAISS + sentence transformers) for patient context, **OpenRouter** for LLM calls, **SQLAlchemy** persistence, and **Twilio** SMS for confirmations and reminders (via APScheduler).

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Twilio](https://img.shields.io/badge/Twilio-F22F46?style=for-the-badge&logo=twilio&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-FF6F00?style=for-the-badge&logo=meta&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=FF9900)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## 📸 Screenshots

<div align="center">

<table>
<tr>
<td align="center" width="55%">

**💬 Telegram Bot — Live Demo**

![Telegram Chat](images/telegram_chat.png)

*Patient lookup, appointment scheduling & natural language commands*

</td>
<td align="center" width="45%">

**📱 Appointment SMS via Twilio**

![SMS Notification](images/sms_notification.png)

*Automated reminder sent 5 hrs before appointment*

</td>
</tr>
</table>

</div>


---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌐 **REST API** | Create, list, read, update, delete patients; schedule appointments |
| 🤖 **Telegram Bot** | Greetings, patient CRUD via intent parsing, free-text appointment scheduling |
| 🧠 **Vector Store (RAG)** | Patient records indexed at startup using FAISS + sentence-transformers |

---

## 📋 Requirements

- Python **3.10+**
- SQL database supported by SQLAlchemy (**PostgreSQL** or **MySQL**)
- [OpenRouter](https://openrouter.ai/) API key for LLM chat completions
- *(Optional)* [Telegram Bot](https://core.telegram.org/bots/tutorial) token
- *(Optional)* [Twilio](https://www.twilio.com/) account for SMS confirmations & reminders

---

## 🚀 Installation

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

> **⚠️ Note:** `twilio` is used by `app/services/sms_service.py` but is not listed in `requirements.txt`; install it explicitly until it is added to the file.

---

## 🔐 Environment Variables

Create a `.env` file in `Dental_Agent/` (same folder as `run_server.py`):

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | SQLAlchemy URL — e.g. `postgresql+psycopg2://user:pass@localhost:5432/dental` |
| `OPEN_ROUTE_API_KEY` | OpenRouter API key (used in `app/integrations/gemini_client.py`) |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather |
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `TWILIO_AUTH_TOKEN` | Twilio auth token |
| `TWILIO_PHONE_NUMBER` | Twilio sender number in E.164 format |

---

## ▶️ Running the Application

> The bot calls the API at `http://127.0.0.1:8000`. **Start the API first**, then the bot in two separate terminals.

### 1. API Server

```bash
cd Dental_Agent
python run_server.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Health check:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **OpenAPI docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Telegram Bot *(optional)*

```bash
cd Dental_Agent
python -m app.bot.run_bot
```

> On startup, the API creates database tables, loads existing patients into the vector index, and starts the reminder scheduler.

---

## 📡 API Reference

### Patients — `/patients`

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/patients/` | Create patient — body: `name`, `phone`, `age`, `gender` |
| `GET` | `/patients/` | List all patients |
| `GET` | `/patients/{patient_id}` | Get one patient by ID |
| `PUT` | `/patients/{patient_id}` | Update patient record |
| `DELETE` | `/patients/{patient_id}` | Delete patient record |

### Appointments — `/appointments`

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/appointments/` | Schedule appointment — body: `patient_id`, `treatment`, `appointment_time` (ISO datetime) |

> ✅ Successful scheduling triggers a **confirmation SMS** via Twilio when configured.

---

## 🗂️ Project Layout

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

---

## 🧪 Tests

```bash
cd Dental_Agent
pytest
```

---

## 🔧 Troubleshooting

| Symptom | Resolution |
|---------|-----------|
| **Bot cannot create patients / appointments** | Ensure the API is running on port `8000` before starting the bot — it uses fixed `http://127.0.0.1:8000` URLs |
| **Database errors on startup** | Verify `DATABASE_URL` is correct and the database exists; drivers must match the URL scheme (`psycopg2` / `pymysql`) |
| **LLM / intent errors** | Check `OPEN_ROUTE_API_KEY` and OpenRouter account limits; intent parsing expects strict JSON from the model |
| **SMS not sending** | Confirm Twilio credentials and that patient phone numbers are valid — the code applies an India `+91` prefix for outbound SMS |

---

<div align="center">

</div>
