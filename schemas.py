"""Modelos Pydantic para validar entradas y salidas."""
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
class SolicitudCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    edad: int = Field(ge=18, le=100)
    salario_mensual: float = Field(gt=0, le=10_000_000)
    tipo_cuenta: Literal["ahorro", "corriente"]
class SolicitudUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=80)
    edad: int | None = Field(default=None, ge=18, le=100)
    salario_mensual: float | None = Field(default=None, gt=0, le=10_000_000)
    tipo_cuenta: Literal["ahorro", "corriente"] | None = None
class SolicitudResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    edad: int
    salario_mensual: float
    tipo_cuenta: str
    califica: bool
    motivo_evaluacion: str
    analisis_ia: str | None = None
class AnalisisResponse(BaseModel):
    solicitud_id: int
    explicacion_ia: str
    analisis_guardado: bool
