from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, dependencies
from ..database import get_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    now = datetime.utcnow()
    last24h = now - timedelta(hours=24)
    total_alerts = db.query(models.Alert).count()
    high_sev = db.query(models.Alert).filter(models.Alert.severity == "high").count()
    open_incidents = db.query(models.Incident).filter(models.Incident.status.in_(["open", "investigating"])).count()
    alerts_last24h = db.query(models.Alert).filter(models.Alert.timestamp >= last24h).count()
    return {
        "total_alerts": total_alerts,
        "high_severity_alerts": high_sev,
        "open_incidents": open_incidents,
        "alerts_last_24h": alerts_last24h,
        "alerts_by_severity": {
            "low": db.query(models.Alert).filter(models.Alert.severity == "low").count(),
            "medium": db.query(models.Alert).filter(models.Alert.severity == "medium").count(),
            "high": high_sev,
            "critical": db.query(models.Alert).filter(models.Alert.severity == "critical").count()
        }
    }