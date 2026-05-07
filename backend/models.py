# backend/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Time, Numeric, Text, CheckConstraint
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
    propietario_id = Column(Integer, ForeignKey("propietarios.id"))
    nombre = Column(String(80), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(80))
    edad_anios = Column(Integer)
    sexo = Column(String(10))
    peso = Column(Numeric(5, 2))
    
    propietario = relationship("Propietario", back_populates="mascotas")
    citas = relationship("Cita", back_populates="paciente")

class Propietario(Base):
    __tablename__ = "propietarios"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    ci = Column(String(20))
    
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