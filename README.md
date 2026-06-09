# AI-Powered SOC Analyst Assistant

## Run with Docker Compose

1. Copy `.env.example` to `.env` and add your OpenAI API key.
2. Run `docker-compose up --build`
3. Frontend: http://localhost:5173
4. Backend API: http://localhost:8000/docs

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