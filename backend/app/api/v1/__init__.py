from fastapi import APIRouter

# Importa los módulos de endpoints v1
# (asegúrate de crear estos archivos: auth.py, votes.py, quorum.py, meetings.py, rules.py)
from . import auth, votes, quorum, meetings, rules

# Router de la versión v1
api_router = APIRouter()

# Monta cada subrouter con su propio prefijo
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(quorum.router, prefix="/quorum", tags=["quorum"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])

__all__ = ["api_router"]
