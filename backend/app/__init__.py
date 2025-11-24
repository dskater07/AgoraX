"""
backend/app/schemas/__init__.py

Paquete de esquemas (Pydantic) del backend AgoraX.

Estos esquemas definen las estructuras de entrada/salida de la API,
desacoplando los modelos de base de datos de las representaciones públicas.
"""

from .user_schema import UserBase, UserCreate, UserRead, Token, TokenData
from .meeting_schema import (
    MeetingCreate,
    MeetingUpdateStatus,
    MeetingSummary,
    MeetingDetail,
    AgendaItemCreate,
    AgendaItemDetail,
    PresenceCreate,
    PresenceSummary,
)
from .vote_schema import VoteCreate, VoteResponse, VoteAggregate
from .audit_schema import AuditLogRead
from .quorum_schema import QuorumStatus, QuorumDetail

__all__ = [
    # Usuarios
    "UserBase",
    "UserCreate",
    "UserRead",
    "Token",
    "TokenData",
    # Reuniones / agenda / presencia
    "MeetingCreate",
    "MeetingUpdateStatus",
    "MeetingSummary",
    "MeetingDetail",
    "AgendaItemCreate",
    "AgendaItemDetail",
    "PresenceCreate",
    "PresenceSummary",
    # Votos
    "VoteCreate",
    "VoteResponse",
    "VoteAggregate",
    # Auditoría
    "AuditLogRead",
    # Quórum
    "QuorumStatus",
    "QuorumDetail",
]
