from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, require_admin
import models, schemas

router = APIRouter(tags=["propietarios"])

@router.get("",response_model=list[schemas.PropietarioOut])
def listar(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.rol == "admin":
        return db.query(models.Propietario).all()
    prop = db.query(models.Propietario).filter(models.Propietario.usuario_id == user.id).first()
    return [prop] if prop else []

@router.post("", response_model=schemas.PropietarioOut)
def crear(data: schemas.PropietarioCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    try:
        # Extraemos los datos del esquema
        datos_propietario = data.model_dump()
        
        # Creamos la instancia del modelo
        p = models.Propietario(**datos_propietario)
        
        # Si tu modelo Propietario tiene una relación con Usuario, 
        # asegúrate de que no sea obligatoria en la DB o asígnale una aquí.
        
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    except Exception as e:
        db.rollback()
        # Esto te dirá exactamente qué falta en la terminal de Python
        print(f"ERROR AL GUARDAR: {str(e)}") 
        raise HTTPException(status_code=400, detail=f"Error en base de datos: {str(e)}")
    
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