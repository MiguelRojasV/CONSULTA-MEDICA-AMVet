from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/api/recetas", tags=["recetas"])

@router.get("/{historial_id}")
def obtener(historial_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Receta).filter(models.Receta.historial_id == historial_id).all()

@router.post("/", response_model=schemas.RecetaOut)
def crear(data: schemas.RecetaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    r = models.Receta(**data.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return r