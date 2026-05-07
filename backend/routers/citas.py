from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/api/citas", tags=["citas"])

@router.get("/")
def listar(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.rol == "admin":
        return db.query(models.Cita).all()
    prop = db.query(models.Propietario).filter(models.Propietario.usuario_id == user.id).first()
    if not prop: return []
    ids = [m.id for m in prop.mascotas]
    return db.query(models.Cita).filter(models.Cita.paciente_id.in_(ids)).all()

@router.post("/", response_model=schemas.CitaOut)
def crear(data: schemas.CitaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = models.Cita(**data.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.put("/{id}", response_model=schemas.CitaOut)
def actualizar(id: int, data: schemas.CitaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(models.Cita).filter(models.Cita.id == id).first()
    if not c: raise HTTPException(404, "No encontrada")
    for k, v in data.model_dump().items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c

@router.delete("/{id}")
def cancelar(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(models.Cita).filter(models.Cita.id == id).first()
    if not c: raise HTTPException(404, "No encontrada")
    c.estado = "cancelada"
    db.commit()
    return {"msg": "Cita cancelada"}