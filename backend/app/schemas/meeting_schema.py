"""
backend/app/schemas/meeting_schema.py

Esquemas Pydantic relacionados con:

- Asambleas (Meeting)
- Puntos de agenda (AgendaItem)
- Presencias (Presence)

Estos esquemas representan la estructura de datos que se envía y recibe
en los endpoints de gestión de asambleas y cálculo de quórum.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ================== AGENDA ITEMS ==================


class AgendaItemBase(BaseModel):
    """
    Esquema base de un punto de agenda.

    No incluye ID ni estado, que se manejan en esquemas más específicos.
    """

    title: str = Field(..., description="Título del punto de agenda.")


class AgendaItemCreate(AgendaItemBase):
    """
    Esquema de entrada para crear un nuevo punto de agenda.

    Se utiliza al momento de definir la agenda de la asamblea.
    """

    pass


class AgendaItemDetail(AgendaItemBase):
    """
    Esquema de salida con detalle de un punto de agenda.

    Incluye:
    - id: identificador del punto.
    - status: estado actual (PENDING / OPEN / CLOSED).
    """

    id: int
    status: str

    class Config:
        from_attributes = True


# ================== PRESENCIAS ==================


class PresenceCreate(BaseModel):
    """
    Esquema de entrada para registrar la presencia de un propietario.

    Este esquema es utilizado por el endpoint que implementa RB-03:
    "El usuario debe confirmar asistencia antes de votar".
    """

    owner_id: int
    meeting_id: int
    coeficiente: float = Field(
        ...,
        description="Coeficiente de copropiedad asociado a este propietario en esta asamblea.",
    )


class PresenceSummary(BaseModel):
    """
    Resumen de una presencia registrada.

    Incluye los campos necesarios para calcular y mostrar el quórum.
    """

    owner_id: int
    owner_name: str
    coeficiente: float
    created_at: datetime

    class Config:
        from_attributes = True


# ================== MEETINGS ==================


class MeetingBase(BaseModel):
    """
    Esquema base para asambleas.

    Incluye:
    - title: título de la asamblea.
    """

    title: str = Field(..., description="Título descriptivo de la asamblea.")


class MeetingCreate(MeetingBase):
    """
    Esquema de entrada para crear una asamblea.

    Campos:
    - condominium_id: conjunto al que pertenece.
    - total_propietarios: número total de propietarios registrados.
    """

    condominium_id: int
    total_propietarios: int = Field(
        ...,
        description="Número total de propietarios (referencia para porcentaje de quórum).",
    )


class MeetingUpdateStatus(BaseModel):
    """
    Esquema de entrada para actualizar el estado de una asamblea.

    Por ejemplo:
        - CREATED → IN_PROGRESS
        - IN_PROGRESS → CLOSED
    """

    status: str = Field(..., description="Nuevo estado de la asamblea.")


class MeetingSummary(BaseModel):
    """
    Resumen de asamblea para listados.

    Incluye:
    - id
    - title
    - date
    - status
    """

    id: int
    title: str
    date: datetime
    status: str

    class Config:
        from_attributes = True


class MeetingDetail(MeetingSummary):
    """
    Detalle completo de una asamblea.

    Extiende MeetingSummary con:
    - condominium_id
    - total_propietarios
    - agenda_items: puntos de agenda asociados.
    """

    condominium_id: int
    total_propietarios: int
    agenda_items: List[AgendaItemDetail] = []
