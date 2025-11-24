"""
backend/app/models/user.py

Modelo de usuario del sistema AgoraX.

Roles:
- ADMIN: administrador del sistema/conjunto.
- OWNER: propietario (votante).

Relación con reglas:
- RD-03: Solo usuarios autenticados pueden votar.
- RB-01: Rol ADMIN controla apertura y cierre de votaciones.
"""

from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from app.core.db import Base


class User(Base):
    """
    Usuario autenticado de AgoraX.

    Atributos:
        id: Identificador interno.
        email: Correo único.
        hashed_password: Contraseña hasheada.
        full_name: Nombre completo.
        role: 'ADMIN' o 'OWNER'.

    Relaciones:
        owner: Propietario asociado (si es OWNER).
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="OWNER")

    owner: Mapped["Owner"] = relationship(
        "Owner",
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )
