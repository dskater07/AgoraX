"""
backend/app/api/v1/__init__.py

Punto de entrada de la versión 1 de la API de AgoraX.

Aquí se agrupan y exponen los routers de los módulos:
- auth.py
- meetings.py
- quorum.py
- rules.py
- votes.py

De esta forma, otros módulos pueden hacer:
    from app.api.v1 import api_router
y montar toda la versión v1 de una sola vez.
"""

from fastapi import APIRouter

# Importa los submódulos que definen sus propios routers
from . import auth, meetings, quorum, rules, votes

# Router principal de la versión v1
api_router = APIRouter()

# Se incluyen los subrouters, asumiendo que cada módulo define `router = APIRouter()`
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(quorum.router, prefix="/quorum", tags=["quorum"])
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])

__all__ = ["api_router"]
