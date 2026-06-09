from sqlalchemy.orm import Session
from ..models import Log, Alert, Incident, AlertSeverity
from ..services.llm_analyzer import explain_alert
from ..services.mitre_mapper import map_to_mitre
import uuid

def analyze_log(log_id: str, db: Session):
    log = db.query(Log).filter(Log.id == log_id).first()
    if not log:
        return

    # Rule-based detection (simple examples)
    if log.event_type == "failed_login":
        # Count recent failed logins from same IP
        recent = db.query(Log).filter(
            Log.source_ip == log.source_ip,
            Log.event_type == "failed_login",
            Log.timestamp >= log.timestamp - interval(minutes=1)
        ).count()
        if recent > 10:
            create_bruteforce_alert(log, db)
    elif log.event_type == "privilege_escalation":
        create_privilege_alert(log, db)
    elif "powershell" in log.raw_log.lower() and "downloadstring" in log.raw_log.lower():
        create_malware_alert(log, db)

def create_bruteforce_alert(log, db):
    description = f"Brute force attack detected from {log.source_ip}: {log.raw_log}"
    mitre = map_to_mitre("bruteforce")
    alert = Alert(
        id=uuid.uuid4(),
        severity=AlertSeverity.HIGH,
        description=description,
        source=f"Source IP: {log.source_ip}",
        mitre_technique=mitre,
        status="new"
    )
    db.add(alert)
    db.commit()
    # Optionally create incident
    inc = Incident(
        title="Brute Force Attack",
        description=description,
        severity=AlertSeverity.HIGH,
        status="open"
    )
    db.add(inc)
    db.commit()
    alert.incident_id = inc.id
    db.commit()

def interval(minutes: int):
    from datetime import timedelta, datetime
    return timedelta(minutes=minutes)