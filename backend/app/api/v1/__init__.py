"""
API Pública v1
--------------

Primera versión estable de la API de AgoraX. Expone recursos y operaciones
para autenticación, asambleas, quórum, votaciones y reglas de negocio.

Convenciones:
    - Prefijo común: /api/v1
    - Subrutas:
        * /auth
        * /meetings
        * /quorum
        * /votes
        * /rules

Trazabilidad:
    - Regulado por reglas RD/RB/RI centralizadas en `rules.py`.
    - Seguridad mediante JWT (ver `auth.py`).
"""

from fastapi import APIRouter

# Importación explícita para registrar subrouters
from . import auth, meetings, quorum, votes, rules  # noqa: F401

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(quorum.router, prefix="/quorum", tags=["quorum"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])

__all__ = ["api_router"]
