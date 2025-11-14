"""
Capa de interfaces HTTP (API)
-----------------------------

Este paquete agrupa los routers de FastAPI y organiza las versiones públicas de
la API (por ejemplo, v1, v2). El router raíz se monta en `main.py` para mantener
el enrutamiento centralizado y facilitar la versionación.

Uso:
    from app.api import root_api_router
    app.include_router(root_api_router)
"""

from fastapi import APIRouter
from .v1 import api_router as v1_router

# Router raíz de la API pública. La versión activa se monta aquí.
root_api_router = APIRouter()
root_api_router.include_router(v1_router, prefix="/api/v1", tags=["v1"])

__all__ = ["root_api_router"]
