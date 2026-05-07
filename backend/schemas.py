from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

# Auth
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    rol: str
    nombre: str
    propietario_id: Optional[int] = None

# Usuario
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str = "propietario"

# Propietario
class PropietarioCreate(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

class PropietarioOut(PropietarioCreate):
    id: int
    class Config:
        from_attributes = True

# Paciente
class PacienteCreate(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[float] = None
    sexo: Optional[str] = None
    peso: Optional[float] = None
    propietario_id: int

class PacienteOut(PacienteCreate):
    id: int
    class Config:
        from_attributes = True

# Cita
class CitaCreate(BaseModel):
    paciente_id: int
    fecha: datetime
    motivo: Optional[str] = None
    tipo: str
    estado: str = "pendiente"
    notas: Optional[str] = None

class CitaOut(CitaCreate):
    id: int
    class Config:
        from_attributes = True

# Historial
class HistorialCreate(BaseModel):
    paciente_id: int
    tipo: str
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    vacuna: Optional[str] = None
    observaciones: Optional[str] = None

class HistorialOut(HistorialCreate):
    id: int
    fecha: datetime
    class Config:
        from_attributes = True

# Receta
class RecetaCreate(BaseModel):
    historial_id: int
    medicamentos: str
    indicaciones: Optional[str] = None

class RecetaOut(RecetaCreate):
    id: int
    fecha_emision: datetime
    class Config:
        from_attributes = True

# Medicamento
class MedicamentoCreate(BaseModel):
    nombre: str
    categoria: Optional[str] = None
    cantidad_stock: int = 0
    unidad: Optional[str] = None
    precio_unitario: Optional[float] = None
    fecha_vencimiento: Optional[date] = None
    descripcion: Optional[str] = None

class MedicamentoOut(MedicamentoCreate):
    id: int
    class Config:
        from_attributes = True

# Seguimiento
class SeguimientoCreate(BaseModel):
    paciente_id: int
    observacion_evolucion: Optional[str] = None
    proximo_control: Optional[datetime] = None
    recomendaciones: Optional[str] = None

class SeguimientoOut(SeguimientoCreate):
    id: int
    fecha_registro: datetime
    class Config:
        from_attributes = True

# Examen
class ExamenCreate(BaseModel):
    paciente_id: int
    tipo_examen: str
    resultado: Optional[str] = None

class ExamenOut(ExamenCreate):
    id: int
    fecha: datetime
    archivo_nombre: Optional[str] = None
    class Config:
        from_attributes = True