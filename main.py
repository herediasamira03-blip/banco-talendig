"""API educativa Banco Talendig."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Solicitud
from schemas import SolicitudCreate, SolicitudUpdate, SolicitudResponse, AnalisisResponse
from services import evaluar_solicitud, generar_explicacion_ia

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas de SQLite al iniciar la aplicación.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Banco Talendig - API Inteligente", version="1.0.0",
              description="Proyecto educativo con FastAPI, SQLite e IA. Utiliza datos ficticios.",
              lifespan=lifespan)

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido a Banco Talendig", "documentacion": "/docs",
            "nota": "Proyecto educativo; no usar para decisiones financieras reales."}

@app.post("/solicitudes", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED, tags=["Solicitudes"])
def crear_solicitud(datos: SolicitudCreate, db: Session = Depends(get_db)):
    # Evalúa la solicitud con las reglas de la práctica.
    resultado = evaluar_solicitud(datos.edad, datos.salario_mensual)
    nueva = Solicitud(nombre=datos.nombre, edad=datos.edad,
        salario_mensual=datos.salario_mensual, tipo_cuenta=datos.tipo_cuenta,
        califica=resultado["califica"], motivo_evaluacion=resultado["motivo"])
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@app.get("/solicitudes", response_model=list[SolicitudResponse], tags=["Solicitudes"])
def listar_solicitudes(db: Session = Depends(get_db)):
    return db.query(Solicitud).order_by(Solicitud.id.asc()).all()

@app.get("/solicitudes/{solicitud_id}", response_model=SolicitudResponse, tags=["Solicitudes"])
def obtener_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if solicitud is None:
        raise HTTPException(status_code=404, detail="La solicitud no existe.")
    return solicitud

@app.put("/solicitudes/{solicitud_id}", response_model=SolicitudResponse, tags=["Solicitudes"])
def actualizar_solicitud(solicitud_id: int, datos: SolicitudUpdate, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if solicitud is None:
        raise HTTPException(status_code=404, detail="La solicitud no existe.")
    # Actualiza únicamente los campos enviados.
    for campo, valor in datos.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(solicitud, campo, valor)
    resultado = evaluar_solicitud(solicitud.edad, solicitud.salario_mensual)
    solicitud.califica = resultado["califica"]
    solicitud.motivo_evaluacion = resultado["motivo"]
    solicitud.analisis_ia = None
    db.commit(); db.refresh(solicitud)
    return solicitud

@app.delete("/solicitudes/{solicitud_id}", tags=["Solicitudes"])
def eliminar_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if solicitud is None:
        raise HTTPException(status_code=404, detail="La solicitud no existe.")
    db.delete(solicitud); db.commit()
    return {"mensaje": "Solicitud eliminada correctamente.", "id": solicitud_id}


@app.post("/solicitudes/{solicitud_id}/analizar", response_model=AnalisisResponse, tags=["Inteligencia artificial"])
def analizar_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()

    if solicitud is None:
        raise HTTPException(status_code=404, detail="La solicitud no existe.")

    try:
        explicacion = generar_explicacion_ia(solicitud)

    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Error de Gemini: {type(error).__name__}: {error}"
        ) from error

    # Guardar el análisis generado por Gemini.
    solicitud.analisis_ia = explicacion
    db.commit()
    db.refresh(solicitud)

    # Devolver la respuesta esperada por FastAPI.
    return {
        "solicitud_id": solicitud.id,
        "explicacion_ia": explicacion,
        "analisis_guardado": True
    }
