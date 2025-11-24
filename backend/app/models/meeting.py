"""
backend/app/models/meeting.py

Modelo de Asamblea (Meeting).

Reglas:
- RD-07: Identificador único por asamblea.
- RD-09: El acta se construye sobre esta entidad.
"""

from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey

from app.core.db import Base


class Meeting(Base):
    """
    Asamblea general de propietarios.

    Atributos:
        id: Identificador.
        condominium_id: FK al conjunto.
        title: Título de la asamblea.
        date: Fecha y hora.
        status: CREATED / IN_PROGRESS / CLOSED.
        total_propietarios: Número total de propietarios de referencia.

    Relaciones:
        condominium: Conjunto asociado.
        agenda_items: Puntos de agenda.
        presences: Asistencias.
    """

    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    condominium_id: Mapped[int] = mapped_column(ForeignKey("condominiums.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="CREATED")
    total_propietarios: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    condominium: Mapped["Condominium"] = relationship(
        "Condominium",
        back_populates="meetings",
        lazy="selectin",
    )
    agenda_items: Mapped[List["AgendaItem"]] = relationship(
        "AgendaItem",
        back_populates="meeting",
        lazy="selectin",
    )
    presences: Mapped[List["Presence"]] = relationship(
        "Presence",
        back_populates="meeting",
        lazy="selectin",
    )
