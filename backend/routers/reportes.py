from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from auth import require_admin
import models

router = APIRouter(prefix="/api/reportes", tags=["reportes"])

@router.get("/resumen")
def resumen(db: Session = Depends(get_db), user=Depends(require_admin)):
    total_pacientes = db.query(func.count(models.Paciente.id)).scalar()
    total_citas = db.query(func.count(models.Cita.id)).scalar()
    citas_pendientes = db.query(func.count(models.Cita.id)).filter(models.Cita.estado == "pendiente").scalar()
    total_propietarios = db.query(func.count(models.Propietario.id)).scalar()
    medicamentos_bajos = db.query(models.Medicamento).filter(models.Medicamento.cantidad_stock < 5).all()
    por_tipo = db.query(models.Cita.tipo, func.count(models.Cita.id)).group_by(models.Cita.tipo).all()
    por_especie = db.query(models.Paciente.especie, func.count(models.Paciente.id)).group_by(models.Paciente.especie).all()
    return {
        "total_pacientes": total_pacientes,
        "total_citas": total_citas,
        "citas_pendientes": citas_pendientes,
        "total_propietarios": total_propietarios,
        "medicamentos_stock_bajo": [{"nombre": m.nombre, "stock": m.cantidad_stock} for m in medicamentos_bajos],
        "citas_por_tipo": [{"tipo": t, "cantidad": c} for t, c in por_tipo],
        "pacientes_por_especie": [{"especie": e, "cantidad": c} for e, c in por_especie],
    }