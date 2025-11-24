"""
backend/app/main.py

Punto de entrada del backend AgoraX.

Aquí se configura:
- La instancia principal de FastAPI.
- El middleware CORS.
- El endpoint de salud (/health).
- La inclusión de todos los routers de la API v1.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import get_settings
from app.core.db import Base, engine
from app.api.v1 import auth, meetings, quorum, rules, votes

settings = get_settings()

# Crear tablas (solo entorno académico/demostración)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AgoraX - Sistema de votación electrónica para Asambleas de Conjuntos "
        "Residenciales (Proyecto académico ITM - Calidad del Software)."
    ),
)

# ================== CORS ==================

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================== ENDPOINTS BÁSICOS ==================

@app.get("/", tags=["system"])
def root():
    """
    Endpoint raíz de referencia.

    Permite verificar rápidamente si el backend está desplegado.
    """
    return {
        "project": "AgoraX",
        "version": settings.APP_VERSION,
        "message": "Backend de AgoraX operativo.",
    }


@app.get("/health", tags=["system"])
def health_check():
    """
    Verifica el estado general de la API y la conexión a la base de datos.

    Ejecuta un SELECT 1 simple para validar el motor de base de datos.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


# ================== REGISTRO DE RUTAS v1 ==================

app.include_router(auth.router)
app.include_router(meetings.router)
app.include_router(quorum.router)
app.include_router(votes.router)
app.include_router(rules.router)
