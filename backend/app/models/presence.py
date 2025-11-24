"""
backend/app/models/presence.py

Modelo de Presencia (asistencia) a la asamblea.

Reglas:
- RB-03: Debe confirmar asistencia antes de votar.
- RD-04: El quórum se calcula a partir de presencias y coeficientes.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, DateTime, ForeignKey, UniqueConstraint

from app.core.db import Base


class Presence(Base):
    """
    Registro de asistencia de un propietario a una asamblea.

    Atributos:
        id: Identificador.
        meeting_id: Asamblea.
        owner_id: Propietario.
        coeficiente: Coeficiente de copropiedad presente.
        created_at: Momento del registro.

    Restricciones:
        - Un propietario solo puede tener una presencia por asamblea.
    """

    __tablename__ = "presences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"), nullable=False)

    coeficiente: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="presences",
        lazy="selectin",
    )
    owner: Mapped["Owner"] = relationship(
        "Owner",
        back_populates="presences",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "meeting_id",
            "owner_id",
            name="uq_presence_meeting_owner",
        ),
    )
