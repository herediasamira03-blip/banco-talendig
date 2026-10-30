"""Conexión y sesiones de SQLite."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
DATABASE_URL = "sqlite:///./banco_talendig.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    # Cada petición obtiene una sesión y se cierra al terminar.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
