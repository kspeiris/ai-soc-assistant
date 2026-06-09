from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, models, dependencies
from ..services import log_ingestion, threat_detector
from ..database import get_db

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post("/ingest", response_model=schemas.LogOut)
def ingest_log(
    log: schemas.LogCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(dependencies.get_current_user)
):
    # Store raw log
    db_log = models.Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    # Async threat detection
    background_tasks.add_task(threat_detector.analyze_log, db_log.id, db)

    return db_log

@router.get("/", response_model=list[schemas.LogOut])
def list_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    return db.query(models.Log).order_by(models.Log.timestamp.desc()).offset(skip).limit(limit).all()