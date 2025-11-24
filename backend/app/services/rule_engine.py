"""
backend/app/services/rule_engine.py

Motor de reglas de negocio para AgoraX.

Este módulo concentra la validación de reglas RD / RB / RI que afectan
operaciones críticas, como emisión de votos y manejo de agenda.

Reglas principales implementadas aquí:
- RD-01: Un propietario solo puede votar una vez por cada punto.
- RD-03: Solo usuarios autenticados pueden votar (complementa security).
- RD-04: El quórum se basa en coeficientes de presencias.
- RD-05: Los resultados no pueden modificarse tras el cierre.
- RD-08: Propietarios con deuda no pueden votar.
- RB-02: Debe cerrarse un punto antes de abrir otro.
- RB-03: El usuario debe confirmar asistencia antes de votar.
- RB-07: No se puede abrir votación sin quórum mínimo.
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Meeting, AgendaItem, Owner, Presence, Vote
from app.services.quorum_service import calculate_quorum

settings = get_settings()


def _http_error(detail: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> HTTPException:
    """
    Crea una excepción HTTP estándar para violaciones de reglas de negocio.
    """
    return HTTPException(status_code=status_code, detail=detail)


def ensure_meeting_allows_voting(meeting: Meeting) -> None:
    """
    Verifica que la asamblea permita operaciones de voto.

    Regla:
        - La asamblea debe estar en estado IN_PROGRESS.
        - Si está CLOSED, no se admite más votación (RD-05).

    Excepción:
        Lanza HTTPException si no se cumple.
    """
    if meeting.status != "IN_PROGRESS":
        raise _http_error(
            f"La asamblea (id={meeting.id}) no está en estado IN_PROGRESS. "
            f"Estado actual: {meeting.status}"
        )


def ensure_agenda_item_is_open(agenda_item: AgendaItem) -> None:
    """
    Verifica que el punto de agenda esté en estado OPEN.

    Regla:
        - El punto debe estar OPEN para admitir nuevos votos.
        - Si está CLOSED, no se admite más votación (RD-05).
    """
    if agenda_item.status != "OPEN":
        raise _http_error(
            f"El punto de agenda (id={agenda_item.id}) no está abierto para votación. "
            f"Estado actual: {agenda_item.status}"
        )


def ensure_owner_not_in_debt(owner: Owner) -> None:
    """
    Verifica que el propietario no tenga deuda pendiente.

    Regla:
        - RD-08: Propietarios con deuda no pueden votar.
    """
    if owner.is_in_debt:
        raise _http_error(
            f"El propietario (id={owner.id}) tiene deuda pendiente y no puede votar."
        )


def ensure_owner_has_presence(db: Session, meeting_id: int, owner_id: int) -> Presence:
    """
    Verifica que el propietario tenga presencia registrada en la asamblea.

    Regla:
        - RB-03: El usuario debe confirmar asistencia antes de votar.

    Retorna:
        El registro de Presence encontrado.

    Excepción:
        Lanza HTTPException si no existe presencia.
    """
    presence: Optional[Presence] = (
        db.query(Presence)
        .filter(
            Presence.meeting_id == meeting_id,
            Presence.owner_id == owner_id,
        )
        .first()
    )

    if presence is None:
        raise _http_error(
            "El propietario no tiene registrada su asistencia en la asamblea, "
            "no puede votar hasta confirmar presencia."
        )

    return presence


def ensure_owner_has_not_voted(
    db: Session,
    agenda_item_id: int,
    owner_id: int,
) -> None:
    """
    Verifica que el propietario no haya votado aún sobre el punto de agenda.

    Regla:
        - RD-01: Un propietario solo puede votar una vez por cada punto.

    Excepción:
        Lanza HTTPException si ya existe un voto previo.
    """
    existing_vote: Optional[Vote] = (
        db.query(Vote)
        .filter(
            Vote.agenda_item_id == agenda_item_id,
            Vote.owner_id == owner_id,
        )
        .first()
    )

    if existing_vote is not None:
        raise _http_error(
            "El propietario ya registró un voto para este punto de agenda."
        )


def ensure_quorum_before_opening_vote(db: Session, meeting: Meeting) -> None:
    """
    Verifica que la asamblea cumpla el quórum mínimo antes de abrir votaciones.

    Regla:
        - RB-07: No se puede abrir votación sin quórum mínimo.
        - RD-04: El quórum se calcula con base en coeficientes de presencia.

    Excepción:
        Lanza HTTPException si el quórum no está cumplido.
    """
    quorum_detail = calculate_quorum(db, meeting_id=meeting.id)
    if not quorum_detail.status.cumple_quorum:
        raise _http_error(
            "No se puede abrir votación: el quórum mínimo aún no está cumplido."
        )


def validate_vote_eligibility(
    db: Session,
    *,
    meeting: Meeting,
    agenda_item: AgendaItem,
    owner: Owner,
) -> None:
    """
    Valida en conjunto todas las reglas necesarias antes de registrar un voto.

    Reglas aplicadas:
        - RD-03: Solo usuarios autenticados pueden votar (se asume ya validado por seguridad).
        - Estado de la asamblea (ensure_meeting_allows_voting).
        - Estado del punto de agenda (ensure_agenda_item_is_open).
        - RD-08: Propietario no debe tener deuda (ensure_owner_not_in_debt).
        - RB-03: Debe tener presencia registrada (ensure_owner_has_presence).
        - RD-01: No debe haber un voto previo sobre el mismo punto (ensure_owner_has_not_voted).

    Si alguna regla no se cumple, se lanza HTTPException con mensaje descriptivo.
    """
    ensure_meeting_allows_voting(meeting)
    ensure_agenda_item_is_open(agenda_item)
    ensure_owner_not_in_debt(owner)
    ensure_owner_has_presence(db, meeting_id=meeting.id, owner_id=owner.id)
    ensure_owner_has_not_voted(db, agenda_item_id=agenda_item.id, owner_id=owner.id)
