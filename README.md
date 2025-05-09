# Dental Call Summarizer

A toy project simulating a dental office call transcription system. The frontend allows manual entry of a call transcript, which is summarized via OpenAI and stored in a database. The call log can be browsed via a web UI.

## Stack

- **Frontend:** React + TailwindCSS (Vite + TypeScript)
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL
- **Infrastructure:** Docker Compose
- **AI Integration:** OpenAI API (summary generation — coming soon)
- **Hosting Target:** AWS (calls.sergeantservices.com)

## Getting Started

### 1. Clone and run:

```bash
git clone https://github.com/your-username/dental-call-summarizer.git
cd dental-call-summarizer
docker compose up --build

