"""
backend/app/models/vote.py

Modelo de Voto.

Reglas:
- RD-01: Un propietario solo puede votar una vez por cada punto.
- RD-06: Los votos se almacenan cifrados.
- RB-06: Registro de IP y timestamp.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint

from app.core.db import Base


class Vote(Base):
    """
    Voto emitido por un propietario sobre un punto de agenda.

    Atributos:
        id: Identificador del voto.
        agenda_item_id: Punto de agenda.
        owner_id: Propietario.
        value_encrypted: Valor cifrado del voto.
        created_at: Fecha/hora del voto.
        ip_address: IP desde la que se emitió.

    Restricciones:
        - Unicidad (agenda_item_id, owner_id) para garantizar RD-01.
    """

    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agenda_item_id: Mapped[int] = mapped_column(ForeignKey("agenda_items.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"), nullable=False)

    value_encrypted: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)

    agenda_item: Mapped["AgendaItem"] = relationship(
        "AgendaItem",
        back_populates="votes",
        lazy="selectin",
    )
    owner: Mapped["Owner"] = relationship(
        "Owner",
        back_populates="votes",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "agenda_item_id",
            "owner_id",
            name="uq_vote_agenda_owner",
        ),
    )
