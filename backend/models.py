# backend/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Time, Numeric, Text, CheckConstraint,Float
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False) # 'admin', 'propietario'
    activo = Column(Boolean, default=True)
    
    # Relación con propietarios
    propietario_perfil = relationship("Propietario", back_populates="usuario", uselist=False)

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    especie = Column(String)
    raza = Column(String, nullable=True)
    edad = Column(Float, nullable=True) # <--- ¡ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ!
    sexo = Column(String, nullable=True)
    peso = Column(Float, nullable=True)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"))
    
    propietario = relationship("Propietario", back_populates="mascotas")
    citas = relationship("Cita", back_populates="paciente")

class Propietario(Base):
    __tablename__ = "propietarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)  # <--- Esta es la columna que faltaba en la tabla
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    correo = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    usuario = relationship("Usuario", back_populates="propietario_perfil")
    mascotas = relationship("Paciente", back_populates="propietario")

class Cita(Base):
    __tablename__ = "citas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    tipo_consulta = Column(String(60)) # 'control', 'vacuna', 'cirugia', etc.
    estado = Column(String(20), default="programada")
    
    paciente = relationship("Paciente", back_populates="citas")