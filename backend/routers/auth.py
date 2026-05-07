from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import verify_password, hash_password, create_token,get_current_user as get_user_from_token

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=schemas.Token)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    propietario_id = None
    if user.propietario_perfil:
        propietario_id = user.propietario_perfil.id
    token = create_token({"sub": user.email, "rol": user.rol})
    return {"access_token": token, "token_type": "bearer", "rol": user.rol, "nombre": user.nombre, "propietario_id": propietario_id}

@router.post("/registro-propietario")
def registro_propietario(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(models.Usuario).filter(models.Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = models.Usuario(nombre=data.nombre, email=data.email,
                          password_hash=hash_password(data.password), rol="propietario")
    db.add(user)
    db.commit()
    db.refresh(user)
    prop = models.Propietario(usuario_id=user.id, nombre=data.nombre, correo=data.email)
    try:
        db.add(prop)
        db.commit()
    except Exception as e:
        db.rollback()
        # Si falla crear el perfil, borramos el usuario para no dejar datos huérfanos
        db.delete(user)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Error al crear perfil: {str(e)}")

    return {"msg": "Propietario registrado correctamente"}
@router.get("/me", response_model=schemas.PropietarioOut)
def read_users_me(
    # Usamos la función que importamos (get_user_from_token)
    current_user: models.Usuario = Depends(get_user_from_token)
):
    return current_user