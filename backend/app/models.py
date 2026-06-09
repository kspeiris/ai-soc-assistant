from sqlalchemy import Column, String, DateTime, Integer, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base
import uuid
import enum

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="analyst")  # admin, analyst, researcher

class Log(Base):
    __tablename__ = "logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    source_ip = Column(String)
    event_type = Column(String, index=True)
    raw_log = Column(Text)
    severity = Column(String, default="info")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    severity = Column(Enum(AlertSeverity))
    description = Column(Text)
    source = Column(String)
    mitre_technique = Column(String, nullable=True)
    status = Column(String, default="new")
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), nullable=True)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(Text)
    severity = Column(Enum(AlertSeverity))
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    report_pdf = Column(String, nullable=True)