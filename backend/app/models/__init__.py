"""
backend/app/models/__init__.py

Paquete de modelos del dominio de AgoraX.

Reexporta las clases principales para facilitar su uso
en otras capas (API, servicios, reglas de negocio).
"""

from .user import User
from .condominum import Condominium
from .owner import Owner
from .meeting import Meeting
from .agenda_item import AgendaItem
from .presence import Presence
from .vote import Vote
from .audit import AuditLog

__all__ = [
    "User",
    "Condominium",
    "Owner",
    "Meeting",
    "AgendaItem",
    "Presence",
    "Vote",
    "AuditLog",
]
