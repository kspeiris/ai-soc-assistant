from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth, logs, alerts, incidents, chat, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI SOC Assistant", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(logs.router)
app.include_router(alerts.router)
app.include_router(incidents.router)
app.include_router(chat.router)
app.include_router(dashboard.router)

@app.get("/health")
def health():
    return {"status": "ok"}