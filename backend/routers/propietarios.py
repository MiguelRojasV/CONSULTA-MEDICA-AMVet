from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, require_admin
import models, schemas

router = APIRouter(prefix="/api/propietarios", tags=["propietarios"])

@router.get("",response_model=list[schemas.PropietarioOut])
def listar(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.rol == "admin":
        return db.query(models.Propietario).all()
    prop = db.query(models.Propietario).filter(models.Propietario.usuario_id == user.id).first()
    return [prop] if prop else []

@router.post("", response_model=schemas.PropietarioOut)
def crear(data: schemas.PropietarioCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    p = models.Propietario(**data.model_dump())
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.put("/{id}", response_model=schemas.PropietarioOut)
def actualizar(id: int, data: schemas.PropietarioCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(models.Propietario).filter(models.Propietario.id == id).first()
    if not p: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump().items():
        setattr(p, k, v)
    db.commit(); db.refresh(p)
    return p

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    p = db.query(models.Propietario).filter(models.Propietario.id == id).first()
    if not p: raise HTTPException(404, "No encontrado")
    db.delete(p); db.commit()
    return {"msg": "Eliminado"}