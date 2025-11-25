"""
backend/app/main.py

Punto de entrada de la aplicación FastAPI para AgoraX.
"""

from fastapi import FastAPI

from app.api import root_api_router
from app.core.db import Base, engine

# Crear tablas (solo para entorno demo/dev; en prod usar migraciones)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgoraX",
    version="1.0.0",
    description="Sistema de votación y quórum para copropiedades.",
)

# Montar la API versionada
app.include_router(root_api_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
