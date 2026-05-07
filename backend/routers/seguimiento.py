from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(tags=["seguimiento"])

@router.get("/{paciente_id}")
def listar(paciente_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Seguimiento).filter(models.Seguimiento.paciente_id == paciente_id).all()

@router.post("/", response_model=schemas.SeguimientoOut)
def crear(data: schemas.SeguimientoCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    s = models.Seguimiento(**data.model_dump())
    db.add(s); db.commit(); db.refresh(s)
    return s