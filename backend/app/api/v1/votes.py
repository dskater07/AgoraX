"""
backend/app/api/v1/votes.py

Endpoints relacionados con el registro y consulta de votos.

Aquí se conectan:
- Modelos: Meeting, AgendaItem, Owner, Vote.
- Esquemas: VoteCreate, VoteResponse.
- Servicios: rule_engine, audit_service.
- Seguridad: cifrado de votos (encrypt_vote_value).

Reglas de negocio aplicadas:
- RD-01: Un propietario solo puede votar una vez por cada punto.
- RD-03: Solo usuarios autenticados pueden votar.
- RD-05: No se puede votar cuando el punto/asamblea está cerrada.
- RD-06: El valor del voto se almacena cifrado.
- RD-08: Propietarios con deuda no pueden votar.
- RB-03: Debe haber presencia registrada antes de votar.
- RB-06: Registrar IP, fecha y hora del voto.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import (
    get_current_user,
    encrypt_vote_value,
)
from app.models import (
    Meeting,
    AgendaItem,
    Owner,
    Vote,
    User,
)
from app.schemas.vote_schema import VoteCreate, VoteResponse
from app.services import audit_service
from app.services import rule_engine

router = APIRouter(prefix="/api/v1/votes", tags=["votes"])


@router.post(
    "/{meeting_id}/agenda/{agenda_item_id}",
    response_model=VoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def cast_vote(
    meeting_id: int,
    agenda_item_id: int,
    vote_in: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Registra un voto para un punto de la agenda.

    Flujo:
        1. Obtiene Meeting, AgendaItem y Owner (a partir de current_user).
        2. Valida elegibilidad de voto mediante rule_engine.validate_vote_eligibility.
        3. Cifra el valor del voto (encrypt_vote_value).
        4. Persiste el voto.
        5. Registra auditoría (audit_service.log_action).

    Si alguna regla se viola, se lanza HTTPException con detalle.
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asamblea no encontrada.",
        )

    agenda_item = (
        db.query(AgendaItem)
        .filter(
            AgendaItem.id == agenda_item_id,
            AgendaItem.meeting_id == meeting_id,
        )
        .first()
    )
    if not agenda_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de agenda no encontrado.",
        )

    owner = db.query(Owner).filter(Owner.user_id == current_user.id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario actual no está asociado a un propietario.",
        )

    # Validar todas las reglas de negocio antes de registrar el voto
    rule_engine.validate_vote_eligibility(
        db=db,
        meeting=meeting,
        agenda_item=agenda_item,
        owner=owner,
    )

    value_encrypted = encrypt_vote_value(vote_in.value)

    vote = Vote(
        agenda_item_id=agenda_item_id,
        owner_id=owner.id,
        value_encrypted=value_encrypted,
        ip_address=vote_in.ip_address,
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)

    audit_service.log_action(
        db,
        user_id=current_user.id,
        action="CAST_VOTE",
        entity_type="Vote",
        entity_id=vote.id,
        description=(
            f"Voto emitido para agenda_item_id={agenda_item_id}, owner_id={owner.id}"
        ),
    )

    return VoteResponse(
        id=vote.id,
        agenda_item_id=vote.agenda_item_id,
        owner_id=vote.owner_id,
        created_at=vote.created_at,
    )


@router.get(
    "/{meeting_id}/agenda/{agenda_item_id}",
    response_model=List[VoteResponse],
)
def list_votes_for_agenda_item(
    meeting_id: int,
    agenda_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve los votos registrados para un punto de agenda.

    NOTA:
        - No expone el valor del voto (value_encrypted).
        - Este endpoint sirve para auditoría básica o validación, no para
          mostrar resultados en claro (eso iría en otra capa agregada).
    """
    agenda_item = (
        db.query(AgendaItem)
        .filter(
            AgendaItem.id == agenda_item_id,
            AgendaItem.meeting_id == meeting_id,
        )
        .first()
    )
    if not agenda_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de agenda no encontrado.",
        )

    votes = (
        db.query(Vote)
        .filter(Vote.agenda_item_id == agenda_item_id)
        .order_by(Vote.created_at.asc())
        .all()
    )

    return [
        VoteResponse(
            id=v.id,
            agenda_item_id=v.agenda_item_id,
            owner_id=v.owner_id,
            created_at=v.created_at,
        )
        for v in votes
    ]
