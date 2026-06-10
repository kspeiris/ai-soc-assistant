# AI-Powered SOC Analyst Assistant

## Run locally without Docker

1. Copy `.env.example` to `.env` in the root and in `backend/` and add your OpenAI API key.
2. Install and start PostgreSQL and Redis locally. Create a database named `soc_db` with user `soc_user` and password `soc_pass` (or update `.env`).
3. Start the Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload
   ```
4. Start the Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
5. Frontend: http://localhost:5173
6. Backend API: http://localhost:8000/docs

## Default User (create via register)
- username: admin
- password: admin123
- role: admin (manually set in DB, or create via /auth/register)

## Features
- Log ingestion (POST /logs/ingest)
- Threat detection (brute force, privilege escalation, malware)
- AI alert explanation
- Incident management and PDF reports
- Chat assistant with RAG (MITRE ATT&CK)
- Interactive dashboard