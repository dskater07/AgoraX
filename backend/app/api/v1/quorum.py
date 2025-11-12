"""
Módulo de Quórum y Asistencia (API v1)
--------------------------------------

Gestiona el registro de asistencia a una asamblea y el cálculo del quórum.
Implementación inicial *in-memory*; lista para migrarse a Redis o PostgreSQL.

Reglas de negocio aplicadas:
    - RD-04: Quórum mínimo (por defecto 51% del total de coeficientes/propietarios).
    - RB-03: El usuario confirma asistencia antes de votar.
    - RB-07: Bloquear apertura de votación si no hay quórum mínimo.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Set

from fastapi import APIRouter, Depends, HTTPException, Query, status

from .auth import PublicUser, get_current_user

router = APIRouter()

# -------------------------------------------------------------------
# Parámetros de negocio (se leen de entorno para facilitar DevOps)
# -------------------------------------------------------------------
TOTAL_PROPIETARIOS: int = int(os.getenv("TOTAL_PROPIETARIOS", "100"))
QUORUM_MIN: float = float(os.getenv("QUORUM_MIN", "51.0"))

# -------------------------------------------------------------------
# Almacenamiento temporal (mock): mapa meeting_id -> set(emails)
# -------------------------------------------------------------------
PRESENCE: Dict[int, Set[str]] = {}


def _ensure_meeting(meeting_id: int) -> Set[str]:
    """Crea el set de presentes si no existe y lo retorna.

    Args:
        meeting_id: Identificador de la asamblea.

    Returns:
        Set[str]: Conjunto de correos de usuarios presentes.
    """
    if meeting_id not in PRESENCE:
        PRESENCE[meeting_id] = set()
    return PRESENCE[meeting_id]


def _status_payload(meeting_id: int) -> dict:
    """Compone el estado de quórum para una asamblea.

    Calcula porcentaje de quórum = (presentes / TOTAL_PROPIETARIOS) * 100.
    Devuelve bandera `estado` como 'válido' si supera el umbral `QUORUM_MIN`.

    Args:
        meeting_id: Identificador de la asamblea.

    Returns:
        dict: Payload con totales, porcentaje, umbral y estado.
    """
    presentes = len(PRESENCE.get(meeting_id, set()))
    porcentaje = (presentes / TOTAL_PROPIETARIOS) * 100 if TOTAL_PROPIETARIOS > 0 else 0.0
    return {
        "meeting_id": meeting_id,
        "total_propietarios": TOTAL_PROPIETARIOS,
        "presentes": presentes,
        "porcentaje_quorum": round(porcentaje, 2),
        "umbral_minimo": QUORUM_MIN,
        "estado": "válido" if porcentaje >= QUORUM_MIN else "inválido",
        "timestamp": datetime.utcnow(),
    }


@router.get("/", summary="Estado del quórum para una asamblea")
def get_quorum(meeting_id: int = Query(..., description="ID de la asamblea")):
    """Obtiene el estado actual del quórum.

    Args:
        meeting_id: Identificador de la asamblea.

    Returns:
        dict: Totales, porcentaje y estado del quórum.
    """
    return _status_payload(meeting_id)


@router.post(
    "/presence",
    status_code=status.HTTP_200_OK,
    summary="Registrar asistencia del usuario autenticado",
)
def register_presence(
    meeting_id: int = Query(..., description="ID de la asamblea"),
    current_user: PublicUser = Depends(get_current_user),
):
    """Registra la asistencia del usuario en la asamblea (RB-03).

    Args:
        meeting_id: Identificador de la asamblea.
        current_user: Usuario autenticado obtenido desde el token.

    Returns:
        dict: Confirmación y estado de quórum tras el registro.
    """
    attendees = _ensure_meeting(meeting_id)
    attendees.add(current_user.email)
    return {
        "message": "Asistencia registrada",
        "meeting_id": meeting_id,
        "user": current_user.email,
        **_status_payload(meeting_id),
    }


@router.delete(
    "/presence",
    status_code=status.HTTP_200_OK,
    summary="Retirar asistencia del usuario autenticado",
)
def remove_presence(
    meeting_id: int = Query(..., description="ID de la asamblea"),
    current_user: PublicUser = Depends(get_current_user),
):
    """Retira la asistencia del usuario autenticado.

    Args:
        meeting_id: Identificador de la asamblea.
        current_user: Usuario autenticado obtenido desde el token.

    Raises:
        HTTPException: 404 si el usuario no estaba registrado como presente.

    Returns:
        dict: Confirmación y estado de quórum tras el retiro.
    """
    attendees = _ensure_meeting(meeting_id)
    if current_user.email not in attendees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no estaba registrado como presente.",
        )
    attendees.remove(current_user.email)
    return {
        "message": "Asistencia retirada",
        "meeting_id": meeting_id,
        "user": current_user.email,
        **_status_payload(meeting_id),
    }


@router.post(
    "/validate",
    status_code=status.HTTP_200_OK,
    summary="Validar apertura de votación según quórum (RB-07)",
)
def validate_open(meeting_id: int = Query(..., description="ID de la asamblea")):
    """Valida si se puede abrir votación de acuerdo al quórum (RB-07).

    Args:
        meeting_id: Identificador de la asamblea.

    Raises:
        HTTPException: 409 si el quórum es insuficiente.

    Returns:
        dict: Mensaje de validación y estado de quórum.
    """
    status_payload = _status_payload(meeting_id)
    if status_payload["estado"] != "válido":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede abrir la votación: quórum inválido "
                   f"({status_payload['porcentaje_quorum']}% < {QUORUM_MIN}%).",
        )
    return {"message": "Validación exitosa: se puede abrir la votación.", **status_payload}
