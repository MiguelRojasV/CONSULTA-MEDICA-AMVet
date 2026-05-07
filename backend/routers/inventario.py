from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, require_admin
import models, schemas

router = APIRouter(tags=["inventario"])

@router.get("/")
def listar(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Medicamento).all()

@router.post("/", response_model=schemas.MedicamentoOut)
def crear(data: schemas.MedicamentoCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    m = models.Medicamento(**data.model_dump())
    db.add(m); db.commit(); db.refresh(m)
    return m

@router.put("/{id}", response_model=schemas.MedicamentoOut)
def actualizar(id: int, data: schemas.MedicamentoCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    m = db.query(models.Medicamento).filter(models.Medicamento.id == id).first()
    if not m: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump().items():
        setattr(m, k, v)
    db.commit(); db.refresh(m)
    return m

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    m = db.query(models.Medicamento).filter(models.Medicamento.id == id).first()
    if not m: raise HTTPException(404, "No encontrado")
    db.delete(m); db.commit()
    return {"msg": "Eliminado"}