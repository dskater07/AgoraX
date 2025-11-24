"""
backend/app/api/v1/meetings.py

Endpoints para la gestión de:

- Asambleas (Meeting)
- Puntos de agenda (AgendaItem)
- Presencias (Presence)

Implementa varios aspectos del ciclo de vida de requerimientos y reglas de negocio:
- Creación de asambleas.
- Cambio de estado (CREATED / IN_PROGRESS / CLOSED).
- Definición de agenda.
- Registro de presencias, base para cálculo de quórum.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.db import get_db
from app.core.security import get_current_user
from app.models import (
    Meeting,
    AgendaItem,
    Presence,
    Owner,
    User,
)
from app.schemas.meeting_schema import (
    MeetingCreate,
    MeetingUpdateStatus,
    MeetingSummary,
    MeetingDetail,
    AgendaItemCreate,
    AgendaItemDetail,
    PresenceCreate,
    PresenceSummary,
)
from app.services.audit_service import log_action

router = APIRouter(prefix="/api/v1/meetings", tags=["meetings"])


# ================== ASAMBLEAS ==================


@router.post("/", response_model=MeetingSummary, status_code=status.HTTP_201_CREATED)
def create_meeting(
    meeting_in: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea una nueva asamblea para un conjunto residencial.

    Regla de negocio relacionada:
        - RD-07: Cada asamblea debe tener un identificador único.
    """
    meeting = Meeting(
        condominium_id=meeting_in.condominium_id,
        title=meeting_in.title,
        total_propietarios=meeting_in.total_propietarios,
        status="CREATED",
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    log_action(
        db,
        user_id=current_user.id,
        action="CREATE_MEETING",
        entity_type="Meeting",
        entity_id=meeting.id,
        description=f"Asamblea creada: {meeting.title}",
    )

    return meeting


@router.get("/", response_model=List[MeetingSummary])
def list_meetings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve el listado de asambleas registradas.

    Se utiliza para la vista general de reuniones.
    """
    meetings = db.query(Meeting).order_by(Meeting.date.desc()).all()
    return meetings


@router.get("/{meeting_id}", response_model=MeetingDetail)
def get_meeting_detail(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve el detalle de una asamblea específica, incluyendo sus puntos de agenda.
    """
    meeting = (
        db.query(Meeting)
        .options(joinedload(Meeting.agenda_items))
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asamblea no encontrada.",
        )

    return meeting


@router.patch("/{meeting_id}/status", response_model=MeetingSummary)
def update_meeting_status(
    meeting_id: int,
    data: MeetingUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza el estado de una asamblea.

    Ejemplos:
        - CREATED → IN_PROGRESS
        - IN_PROGRESS → CLOSED

    Reglas:
        - RD-05: Los resultados no se modifican tras el cierre. El cambio a CLOSED
          debe considerarse definitivo en el flujo de negocio.
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asamblea no encontrada.",
        )

    meeting.status = data.status
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    log_action(
        db,
        user_id=current_user.id,
        action="UPDATE_MEETING_STATUS",
        entity_type="Meeting",
        entity_id=meeting.id,
        description=f"Estado actualizado a {meeting.status}",
    )

    return meeting


# ================== AGENDA ITEMS ==================


@router.post(
    "/{meeting_id}/agenda",
    response_model=AgendaItemDetail,
    status_code=status.HTTP_201_CREATED,
)
def add_agenda_item(
    meeting_id: int,
    item_in: AgendaItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Agrega un nuevo punto de agenda a una asamblea.

    Regla relacionada:
        - RB-02 se implementa en la lógica de aperturas/cierres de puntos,
          no en la creación.
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asamblea no encontrada.",
        )

    agenda_item = AgendaItem(
        meeting_id=meeting_id,
        title=item_in.title,
        status="PENDING",
    )
    db.add(agenda_item)
    db.commit()
    db.refresh(agenda_item)

    log_action(
        db,
        user_id=current_user.id,
        action="ADD_AGENDA_ITEM",
        entity_type="AgendaItem",
        entity_id=agenda_item.id,
        description=f"Punto de agenda creado: {agenda_item.title}",
    )

    return agenda_item


@router.patch(
    "/{meeting_id}/agenda/{agenda_item_id}/status",
    response_model=AgendaItemDetail,
)
def update_agenda_item_status(
    meeting_id: int,
    agenda_item_id: int,
    data: MeetingUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza el estado de un punto de agenda.

    Aquí se materializa parte de RB-02:
        - Debe cerrarse un punto antes de abrir otro (validación adicional
          podría implementarse en rule_engine si se requiere).
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

    agenda_item.status = data.status
    db.add(agenda_item)
    db.commit()
    db.refresh(agenda_item)

    log_action(
        db,
        user_id=current_user.id,
        action="UPDATE_AGENDA_ITEM_STATUS",
        entity_type="AgendaItem",
        entity_id=agenda_item.id,
        description=f"Estado del punto actualizado a {agenda_item.status}",
    )

    return agenda_item


# ================== PRESENCES ==================


@router.post(
    "/{meeting_id}/presence",
    response_model=PresenceSummary,
    status_code=status.HTTP_201_CREATED,
)
def register_presence(
    meeting_id: int,
    presence_in: PresenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Registra la presencia de un propietario en una asamblea.

    Reglas relacionadas:
        - RB-03: El usuario debe confirmar asistencia antes de votar.
        - RD-04: El coeficiente se usa para el cálculo de quórum.
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asamblea no encontrada.",
        )

    owner = db.query(Owner).filter(Owner.id == presence_in.owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Propietario no encontrado.",
        )

    presence = Presence(
        meeting_id=meeting_id,
        owner_id=presence_in.owner_id,
        coeficiente=presence_in.coeficiente,
    )
    db.add(presence)
    db.commit()
    db.refresh(presence)

    log_action(
        db,
        user_id=current_user.id,
        action="REGISTER_PRESENCE",
        entity_type="Presence",
        entity_id=presence.id,
        description=(
            f"Presencia registrada para owner_id={owner.id}, "
            f"coeficiente={presence.coeficiente}"
        ),
    )

    return PresenceSummary(
        owner_id=owner.id,
        owner_name=owner.name,
        coeficiente=presence.coeficiente,
        created_at=presence.created_at,
    )
