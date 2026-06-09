from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional
from .models import AlertSeverity, IncidentStatus

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: UUID4
    username: str
    email: str
    role: str

class LogCreate(BaseModel):
    source_ip: str
    event_type: str
    raw_log: str
    severity: Optional[str] = "info"

class LogOut(LogCreate):
    id: UUID4
    timestamp: datetime

class AlertOut(BaseModel):
    id: UUID4
    timestamp: datetime
    severity: AlertSeverity
    description: str
    source: str
    mitre_technique: Optional[str]
    status: str
    incident_id: Optional[UUID4]

class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: AlertSeverity

class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus]
    resolved_at: Optional[datetime]

class IncidentOut(BaseModel):
    id: UUID4
    title: str
    description: str
    severity: AlertSeverity
    status: IncidentStatus
    created_at: datetime
    resolved_at: Optional[datetime]

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None