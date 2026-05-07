from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/api/historial", tags=["historial"])

@router.get("/{paciente_id}")
def listar(paciente_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.HistorialClinico).filter(models.HistorialClinico.paciente_id == paciente_id).all()

@router.post("/", response_model=schemas.HistorialOut)
def crear(data: schemas.HistorialCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    h = models.HistorialClinico(**data.model_dump())
    db.add(h); db.commit(); db.refresh(h)
    return h