"""
backend/app/models/audit.py

Modelo de auditoría (AuditLog).

Permite registrar acciones clave para trazabilidad del proceso,
en línea con requisitos de transparencia y control.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text

from app.core.db import Base


class AuditLog(Base):
    """
    Registro de auditoría de eventos relevantes en AgoraX.

    Atributos:
        id: Identificador.
        user_id: Usuario que ejecutó la acción (opcional).
        action: Código de la acción.
        entity_type: Tipo de entidad afectada (Meeting, Vote, etc.).
        entity_id: ID de la entidad afectada.
        description: Detalle adicional.
        created_at: Fecha y hora del evento.
    """

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
