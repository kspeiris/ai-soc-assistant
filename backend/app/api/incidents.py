from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, dependencies
from ..database import get_db
from ..services.report_generator import generate_incident_report

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=schemas.IncidentOut)
def create_incident(inc: schemas.IncidentCreate, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    db_inc = models.Incident(**inc.dict())
    db.add(db_inc)
    db.commit()
    db.refresh(db_inc)
    return db_inc

@router.get("/", response_model=list[schemas.IncidentOut])
def list_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    return db.query(models.Incident).order_by(models.Incident.created_at.desc()).offset(skip).limit(limit).all()

@router.patch("/{incident_id}", response_model=schemas.IncidentOut)
def update_incident(incident_id: str, update: schemas.IncidentUpdate, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    inc = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404)
    for key, value in update.dict(exclude_unset=True).items():
        setattr(inc, key, value)
    db.commit()
    db.refresh(inc)
    return inc

@router.get("/{incident_id}/report")
def download_report(incident_id: str, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    inc = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404)
    pdf_bytes = generate_incident_report(inc)
    from fastapi.responses import StreamingResponse
    import io
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=incident_{incident_id}.pdf"})