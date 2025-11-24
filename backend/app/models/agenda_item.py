"""
backend/app/models/agenda_item.py

Modelo de Punto de Agenda (AgendaItem).

Reglas:
- RB-02: Debe cerrarse un punto antes de abrir otro.
- RB-09: Resultados visibles cuando todos los puntos estén cerrados.
"""

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from app.core.db import Base


class AgendaItem(Base):
    """
    Punto de agenda de una asamblea.

    Atributos:
        id: Identificador.
        meeting_id: Asamblea a la que pertenece.
        title: Título del punto.
        status: PENDING / OPEN / CLOSED.

    Relaciones:
        meeting: Asamblea asociada.
        votes: Votos asociados.
    """

    __tablename__ = "agenda_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="PENDING")

    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="agenda_items",
        lazy="selectin",
    )
    votes: Mapped[List["Vote"]] = relationship(
        "Vote",
        back_populates="agenda_item",
        lazy="selectin",
    )
