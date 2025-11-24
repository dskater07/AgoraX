"""
backend/app/models/condominum.py

Modelo de Conjunto Residencial (Condominium).

Reglas relacionadas:
- RD-10: Cada conjunto tiene un coeficiente total.
- RD-04: El coeficiente total se usa en el cálculo de quórum.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float

from app.core.db import Base


class Condominium(Base):
    """
    Conjunto Residencial administrado por AgoraX.

    Atributos:
        id: Identificador del conjunto.
        name: Nombre del conjunto.
        coeficiente_total: Suma de coeficientes de todos los propietarios.

    Relaciones:
        owners: Lista de propietarios.
        meetings: Lista de asambleas.
    """

    __tablename__ = "condominiums"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    coeficiente_total: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)

    owners: Mapped[list["Owner"]] = relationship(
        "Owner",
        back_populates="condominium",
        lazy="selectin",
    )
    meetings: Mapped[list["Meeting"]] = relationship(
        "Meeting",
        back_populates="condominium",
        lazy="selectin",
    )
