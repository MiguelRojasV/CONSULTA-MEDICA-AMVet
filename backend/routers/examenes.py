from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, aiofiles, os

router = APIRouter(tags=["examenes"])
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/{paciente_id}")
def listar(paciente_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Examen).filter(models.Examen.paciente_id == paciente_id).all()

@router.post("/")
async def crear(
    paciente_id: int = Form(...),
    tipo_examen: str = Form(...),
    resultado: str = Form(""),
    archivo: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    archivo_nombre = None
    archivo_ruta = None
    if archivo:
        archivo_nombre = archivo.filename
        archivo_ruta = os.path.join(UPLOAD_DIR, archivo.filename)
        async with aiofiles.open(archivo_ruta, 'wb') as f:
            await f.write(await archivo.read())
    e = models.Examen(paciente_id=paciente_id, tipo_examen=tipo_examen,
                      resultado=resultado, archivo_nombre=archivo_nombre, archivo_ruta=archivo_ruta)
    db.add(e); db.commit(); db.refresh(e)
    return e