"""
backend/app/core/db.py

Gestión de la conexión a la base de datos usando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Base declarativa para los modelos SQLAlchemy."""
    pass


DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependencia FastAPI para obtener una sesión de BD.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
