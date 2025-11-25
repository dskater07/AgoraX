"""
backend/app/__init__.py

Inicializa el paquete principal del backend AgoraX.
Expone la instancia de FastAPI como `app` para Uvicorn.
"""

from .main import app  # noqa: F401
