from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, dependencies
from ..services import log_ingestion, threat_detector
from ..database import get_db
from fastapi import HTTPException
import traceback

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post("/ingest")
def ingest_log(
    log: schemas.LogCreate,
    db: Session = Depends(get_db),
    current_user = None
):
    try:
        # Store raw log
        db_log = models.Log(**log.model_dump())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        return {
            "id": str(db_log.id),
            "timestamp": db_log.timestamp,
            "source_ip": db_log.source_ip,
            "event_type": db_log.event_type,
            "raw_log": db_log.raw_log,
            "severity": db_log.severity,
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[schemas.LogOut])
def list_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    return db.query(models.Log).order_by(models.Log.timestamp.desc()).offset(skip).limit(limit).all()
