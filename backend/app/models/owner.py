"""
backend/app/models/owner.py

Modelo de Propietario.

Reglas relacionadas:
- RD-08: Propietarios con deuda no pueden votar.
- RD-04/RD-10: El coeficiente de cada propietario contribuye al quórum.
"""

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey

from app.core.db import Base


class Owner(Base):
    """
    Propietario de una unidad privada dentro del conjunto.

    Atributos:
        id: Identificador.
        user_id: FK a User.
        condominium_id: FK a Condominium.
        name: Nombre del propietario.
        coeficiente: Coeficiente de copropiedad.
        is_in_debt: Indica si tiene deuda (afecta RD-08).

    Relaciones:
        user: Usuario asociado.
        condominium: Conjunto asociado.
        presences: Asistencias a asambleas.
        votes: Votos emitidos.
    """

    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    condominium_id: Mapped[int] = mapped_column(ForeignKey("condominiums.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    coeficiente: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    is_in_debt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="owner",
        lazy="selectin",
    )
    condominium: Mapped["Condominium"] = relationship(
        "Condominium",
        back_populates="owners",
        lazy="selectin",
    )
    presences: Mapped[List["Presence"]] = relationship(
        "Presence",
        back_populates="owner",
        lazy="selectin",
    )
    votes: Mapped[List["Vote"]] = relationship(
        "Vote",
        back_populates="owner",
        lazy="selectin",
    )
