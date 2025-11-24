"""
backend/app/services/quorum_service.py

Servicio para el cálculo de quórum en AgoraX.

Este módulo encapsula la lógica necesaria para:
- Calcular el porcentaje de quórum de una asamblea.
- Saber si se cumple el mínimo establecido (RD-04).
- Devolver un detalle útil para el frontend y la auditoría.

Reglas de negocio relacionadas:
- RD-04: El quórum mínimo es del 51% del coeficiente total.
- RD-10: Cada conjunto debe registrar su coeficiente total.
- RB-03: La presencia se usa como base para el quórum.
"""

from typing import List, Dict, Any

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.core.config import get_settings
from app.models import Meeting, Condominium, Presence, Owner
from app.schemas.quorum_schema import QuorumStatus, QuorumDetail

settings = get_settings()


def calculate_quorum(db: Session, meeting_id: int) -> QuorumDetail:
    """
    Calcula el estado de quórum para una asamblea dada.

    Lógica:
        - Obtiene la asamblea y su conjunto.
        - Suma los coeficientes de todos los propietarios presentes (Presence).
        - Usa el coeficiente_total del conjunto para el denominador.
        - Calcula el porcentaje de quórum.
        - Compara contra QUORUM_MIN (por defecto 51%).

    Parámetros:
        db: Sesión de base de datos.
        meeting_id: ID de la asamblea.

    Retorna:
        QuorumDetail con:
        - status: información agregada de quórum.
        - presentes: listado simple de presencias que contribuyen al quórum.

    Excepciones:
        - ValueError si la asamblea no existe o no tiene conjunto asociado.
    """
    meeting: Meeting | None = (
        db.query(Meeting)
        .options(
            joinedload(Meeting.condominium),
            joinedload(Meeting.presences).joinedload(Presence.owner),
        )
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if meeting is None:
        raise ValueError(f"Asamblea con id {meeting_id} no encontrada.")

    condominium: Condominium | None = meeting.condominium
    if condominium is None:
        raise ValueError(
            f"Asamblea {meeting_id} no está asociada a un conjunto (Condominium)."
        )

    coeficiente_total = condominium.coeficiente_total or 0.0

    # Sumar coeficientes de presencias
    presentes_coeficiente = (
        db.query(func.coalesce(func.sum(Presence.coeficiente), 0.0))
        .filter(Presence.meeting_id == meeting_id)
        .scalar()
    )

    if coeficiente_total <= 0:
        porcentaje_quorum = 0.0
    else:
        porcentaje_quorum = (presentes_coeficiente / coeficiente_total) * 100.0

    cumple_quorum = porcentaje_quorum >= settings.QUORUM_MIN

    status = QuorumStatus(
        meeting_id=meeting_id,
        presentes_coeficiente=float(presentes_coeficiente),
        coeficiente_total=float(coeficiente_total),
        porcentaje_quorum=float(round(porcentaje_quorum, 2)),
        cumple_quorum=bool(cumple_quorum),
    )

    # Detalle de presentes (para UI / reportes)
    presentes_list: List[Dict[str, Any]] = []
    for presence in meeting.presences:
        owner: Owner | None = presence.owner
        presentes_list.append(
            {
                "owner_id": owner.id if owner else None,
                "owner_name": owner.name if owner else "Desconocido",
                "coeficiente": presence.coeficiente,
                "created_at": presence.created_at,
            }
        )

    return QuorumDetail(status=status, presentes=presentes_list)
