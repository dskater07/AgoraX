"""
Capa de interfaces HTTP (API)
-----------------------------
"""

from fastapi import APIRouter
from app.api.v1 import api_router as v1_router

root_api_router = APIRouter()
root_api_router.include_router(v1_router, prefix="/api/v1", tags=["v1"])

__all__ = ["root_api_router"]
