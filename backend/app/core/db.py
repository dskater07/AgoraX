"""
backend/app/core/db.py

Módulo de conexión a base de datos para AgoraX.

Define:
- Base: clase base de modelos SQLAlchemy.
- engine: motor de conexión a PostgreSQL.
- SessionLocal: fábrica de sesiones.
- get_db: dependencia reutilizable para FastAPI.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """
    Clase base para todos los modelos de AgoraX.

    Todos los modelos deben heredar de Base para que SQLAlchemy
    pueda crear y gestionar las tablas.
    """
    pass


DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# Motor de conexión
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependencia FastAPI que proporciona una sesión de base de datos.

    Ejemplo de uso:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
