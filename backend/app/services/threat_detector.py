from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models import Log, Alert, Incident, AlertSeverity
from ..services.llm_analyzer import explain_alert
from ..services.mitre_mapper import map_to_mitre
import uuid

def analyze_log(log_id: str, db: Session):
    log = db.query(Log).filter(Log.id == log_id).first()
    if not log:
        return

    # Rule-based detection
    if log.event_type == "failed_login":
        # Count recent failed logins from same IP within 1 minute
        one_min_ago = datetime.utcnow() - timedelta(minutes=1)
        recent = db.query(Log).filter(
            Log.source_ip == log.source_ip,
            Log.event_type == "failed_login",
            Log.timestamp >= one_min_ago
        ).count()
        if recent >= 10:
            create_bruteforce_alert(log, db)
    elif log.event_type == "privilege_escalation":
        create_privilege_alert(log, db)
    elif "powershell" in log.raw_log.lower() and "downloadstring" in log.raw_log.lower():
        create_malware_alert(log, db)
    elif log.event_type == "port_scan":
        create_portscan_alert(log, db)

def create_bruteforce_alert(log, db):
    description = f"Brute force attack detected from {log.source_ip}: {log.raw_log[:200]}"
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
    # Create incident
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

def create_privilege_alert(log, db):
    description = f"Privilege escalation detected: {log.raw_log[:200]}"
    mitre = map_to_mitre("privilege_escalation")
    alert = Alert(
        id=uuid.uuid4(),
        severity=AlertSeverity.CRITICAL,
        description=description,
        source=log.source_ip,
        mitre_technique=mitre,
        status="new"
    )
    db.add(alert)
    db.commit()
    inc = Incident(
        title="Privilege Escalation",
        description=description,
        severity=AlertSeverity.CRITICAL,
        status="open"
    )
    db.add(inc)
    db.commit()
    alert.incident_id = inc.id
    db.commit()

def create_malware_alert(log, db):
    description = f"Possible malware indicator: {log.raw_log[:200]}"
    mitre = map_to_mitre("malware")
    alert = Alert(
        id=uuid.uuid4(),
        severity=AlertSeverity.HIGH,
        description=description,
        source=log.source_ip,
        mitre_technique=mitre,
        status="new"
    )
    db.add(alert)
    db.commit()
    inc = Incident(
        title="Malware Detected",
        description=description,
        severity=AlertSeverity.HIGH,
        status="open"
    )
    db.add(inc)
    db.commit()
    alert.incident_id = inc.id
    db.commit()

def create_portscan_alert(log, db):
    description = f"Port scanning detected from {log.source_ip}"
    mitre = map_to_mitre("lateral_movement")
    alert = Alert(
        id=uuid.uuid4(),
        severity=AlertSeverity.MEDIUM,
        description=description,
        source=log.source_ip,
        mitre_technique=mitre,
        status="new"
    )
    db.add(alert)
    db.commit()