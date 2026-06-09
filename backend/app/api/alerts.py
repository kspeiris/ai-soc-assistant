from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, dependencies
from ..database import get_db

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=list[schemas.AlertOut])
def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    return db.query(models.Alert).order_by(models.Alert.timestamp.desc()).offset(skip).limit(limit).all()

@router.get("/{alert_id}", response_model=schemas.AlertOut)
def get_alert(alert_id: str, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404)
    return alert

@router.post("/{alert_id}/resolve")
def resolve_alert(alert_id: str, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404)
    alert.status = "resolved"
    db.commit()
    return {"status": "resolved"}