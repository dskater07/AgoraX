"""
backend/app/models/__init__.py

Inicializa el paquete de modelos SQLAlchemy de AgoraX.

Se importan explícitamente los modelos principales para garantizar su
disponibilidad sin depender de `import *`, que es frágil y silencioso.
"""

# Importación explícita de todos los modelos
from .user import User
from .meeting import Meeting
from .agenda_item import AgendaItem
from .condominium import Condominium
from .owner import Owner
from .presence import Presence
from .vote import Vote
from .audit import AuditLog

__all__ = [
    "User",
    "Meeting",
    "AgendaItem",
    "Condominium",
    "Owner",
    "Presence",
    "Vote",
    "AuditLog",
]
