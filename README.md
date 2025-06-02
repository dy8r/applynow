# ApplyNow.dev 🧑‍💻

ApplyNow is an open-source microservice-based job alert platform built to help job seekers — especially in Winnipeg — stay ahead of job postings from top tech companies.

It scrapes company job boards, enriches listings with AI, and alerts users via Telegram — all fully automated and free.

You can use it live at [applynow.dev](https://applynow.dev)
Get alerts in [Telegram](https://t.me/applynowalerts_bot)

---

## frontend/

- **Tech**: React + TypeScript + TailwindCSS
- **Purpose**: Public web interface for browsing jobs
- **Features**: Mobile-first UI, Telegram login, beautiful job display

### How to run:
```bash
cd frontend
cp .env.test .env
npm install
npm run dev
```
---

## backend/

- **Tech**: FastAPI + PostgreSQL
- **Purpose**: REST API layer for job listings, filters and analytics
- **Features**: Fast endpoints, usage tracking

### How to run:
```bash
cd backend
cp .env.test .env
uvicorn main:app --reload
```
---

## crawler/

- **Tech**: Python + BeautifulSoup + Requests
- **Purpose**: Scrapes jobs from companies like Neo, Payworks, Pollard, and others
- **Features**: Async-friendly, de-duplication, AI-enriched job descriptions

### How to run:
```bash
cd crawler
cp .env.test .env
python run.py
```
---


## db/

- **Tech**: SQL
- **Purpose**: Contains schema definition and migration scripts for PostgreSQL
- **Features**: Clean, optimized schema with analytics tracking and job filters

### How to set up:
- Launch a PostgreSQL database
- Run the schema from `db/schema.sql`
- Or just `python3 __init__.py`
---

## tgalerts/

- **Tech**: Python + Telethon
- **Purpose**: Sends new job alerts to Telegram users based on preferences
- **Features**: Filtered alerts, deduplication, works in sync with tgbot

### How to run:
```bash
cd tgalerts
cp .env.test .env
python main.py
```
---

## tgbot/

- **Tech**: Python + Telethon
- **Purpose**: Interactive Telegram bot for user onboarding and alert filter management
- **Features**: Inline buttons, dynamic toggles, feedback via bot

### How to run:
```bash
cd tgbot
cp .env.test .env
python bot.py
```
---

## Setup Instructions

1. Go into each folder (`frontend/`, `backend/`, etc.)
2. Copy `.env.test` to `.env`
3. Fill in real values (DB URL, tokens, Telegram credentials, etc.)
4. Follow run commands for each service

Each microservice is standalone and can be scaled independently.
---

## Final Notes

- 💡 AI enriches each job post with title, tags, salary range, and work model
- 🛠️ Easily extensible to more companies and locations
- 🔓 100% free & open source
- 🌐 Live: [applynow.dev](https://applynow.dev)
- 🧑‍💻 GitHub: [github.com/dy8r/applynow](https://github.com/dy8r/applynow)
