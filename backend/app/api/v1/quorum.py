from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from typing import Dict, Set, List
import os

from .auth import get_current_user, PublicUser

router = APIRouter()

# ================================
# Configuración básica
# ================================
TOTAL_PROPIETARIOS = int(os.getenv("TOTAL_PROPIETARIOS", "100"))
QUORUM_MIN = float(os.getenv("QUORUM_MIN", "51.0"))  # Regla RD-04

# Presencia en memoria por meeting_id
# Ej: PRESENCE[1] = {"admin@agorax.com", "vecino@cr.com"}
PRESENCE: Dict[int, Set[str]] = {}


def _ensure_meeting(meeting_id: int) -> Set[str]:
    if meeting_id not in PRESENCE:
        PRESENCE[meeting_id] = set()
    return PRESENCE[meeting_id]


def _status_payload(meeting_id: int) -> dict:
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


# ================================
# Endpoints
# ================================

@router.get("/", summary="Estado del quorum para una asamblea")
def get_quorum(
    meeting_id: int = Query(..., description="ID de la asamblea")
):
    """
    Retorna el estado de quorum para la asamblea indicada.
    Cumple RD-04 (quorum mínimo) y soporta RB-07 (bloquear apertura sin quorum).
    """
    return _status_payload(meeting_id)


@router.post("/presence", summary="Registrar asistencia del usuario actual")
def register_presence(
    meeting_id: int = Query(..., description="ID de la asamblea"),
    current_user: PublicUser = Depends(get_current_user),
):
    """
    Marca presente al usuario autenticado en la asamblea.
    Útil para confirmar asistencia antes de votar (RB-03).
    """
    attendees = _ensure_meeting(meeting_id)
    attendees.add(current_user.email)
    return {
        "message": "Asistencia registrada",
        "meeting_id": meeting_id,
        "user": current_user.email,
        **_status_payload(meeting_id),
    }


@router.delete("/presence", summary="Retirar asistencia del usuario actual")
def remove_presence(
    meeting_id: int = Query(..., description="ID de la asamblea"),
    current_user: PublicUser = Depends(get_current_user),
):
    """
    Retira al usuario autenticado de la lista de presentes.
    """
    attendees = _ensure_meeting(meeting_id)
    if current_user.email in attendees:
        attendees.remove(current_user.email)
        return {
            "message": "Asistencia retirada",
            "meeting_id": meeting_id,
            "user": current_user.email,
            **_status_payload(meeting_id),
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no estaba registrado como presente.")


@router.get("/present-list", summary="Listar correos de asistentes presentes (demo)")
def present_list(
    meeting_id: int = Query(..., description="ID de la asamblea"),
):
    """
    Lista simple de presentes (para auditoría rápida o debugging).
    En producción, esta info debería ser limitada a roles autorizados.
    """
    return {
        "meeting_id": meeting_id,
        "presentes": sorted(list(PRESENCE.get(meeting_id, set()))),
        "count": len(PRESENCE.get(meeting_id, set())),
        "timestamp": datetime.utcnow(),
    }


@router.post("/validate", summary="Validar si se puede abrir votación (bloquea sin quorum)")
def validate_open(
    meeting_id: int = Query(..., description="ID de la asamblea"),
):
    """
    Verifica la regla RB-07: no se puede abrir votación si no hay quorum mínimo.
    """
    status_payload = _status_payload(meeting_id)
    if status_payload["estado"] != "válido":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede abrir la votación: quorum inválido ({status_payload['porcentaje_quorum']}% < {QUORUM_MIN}%).",
        )
    return {
        "message": "Validación exitosa: se puede abrir la votación.",
        **status_payload,
    }
