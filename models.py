"""Tabla de solicitudes guardada en SQLite."""
from sqlalchemy import Boolean, Column, Float, Integer, String, Text
from database import Base
class Solicitud(Base):
    __tablename__ = "solicitudes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), nullable=False)
    edad = Column(Integer, nullable=False)
    salario_mensual = Column(Float, nullable=False)
    tipo_cuenta = Column(String(30), nullable=False)
    califica = Column(Boolean, nullable=False)
    motivo_evaluacion = Column(String(250), nullable=False)
    analisis_ia = Column(Text, nullable=True)
