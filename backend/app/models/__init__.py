"""
backend/app/models/__init__.py

Paquete de modelos ORM del sistema AgoraX.

Los modelos representan las entidades persistentes en la base de datos,
implementadas con SQLAlchemy. Este archivo expone únicamente los módulos
del paquete, sin importar clases directamente, para evitar ciclos de 
dependencia entre modelos, esquemas y servicios.

Modelos incluidos:
- user.py
- owner.py
- condominium.py
- meeting.py
- agenda_item.py
- presence.py
- vote.py
- audit.py
"""

__all__ = [
    "user",
    "owner",
    "condominium",
    "meeting",
    "agenda_item",
    "presence",
    "vote",
    "audit",
]
