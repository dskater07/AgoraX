"""
backend/app/schemas/audit_schema.py

Esquemas Pydantic relacionados con la auditoría (AuditLog).

Se usan principalmente en endpoints internos o vistas
que quieran mostrar el historial de acciones relevantes.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuditLogRead(BaseModel):
    """
    Esquema de lectura de un registro de auditoría.

    No se define esquema de creación porque en general
    los registros se generan desde la capa de servicios.
    """

    id: int
    user_id: Optional[int]
    action: str
    entity_type: str
    entity_id: Optional[int]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
