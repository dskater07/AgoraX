"""
backend/app/api/v1/__init__.py

Paquete de la versión 1 de la API de AgoraX.

Contiene los routers:
- auth: Autenticación y gestión básica de usuarios.
- meetings: Gestión de asambleas, agenda y presencias.
- quorum: Cálculo de quórum.
- votes: Registro de votos y consulta de resultados.
- rules: Exposición de reglas de negocio (RD, RB, RI).
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")
