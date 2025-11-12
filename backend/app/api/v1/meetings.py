"""
Módulo de Asambleas (API v1)
----------------------------

Gestiona el ciclo de vida de una asamblea: creación, consulta y
transiciones de estado (pendiente → abierta → cerrada).

Reglas de negocio aplicadas:
    - RD-04: Quorum mínimo de referencia en la entidad.
    - RD-07: Cada asamblea dispone de un identificador único.
    - RB-01: Solo el administrador puede abrir/cerrar asambleas.
    - RB-02: Debe cerrarse una asamblea antes de abrir otra.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from .auth import PublicUser, get_current_user
from app.schemas.meeting_schema import (
    MeetingCreate,
    MeetingOut,
    MeetingUpdate,
    MeetingStatusEnum,
)

router = APIRouter()

# -------------------------------------------------------------------
# Almacenamiento temporal (mock). Reemplazar por persistencia real.
# -------------------------------------------------------------------
MEETINGS: list[dict] = []


def _get_meeting(meeting_id: int) -> dict | None:
    """Obtiene una asamblea por ID desde almacenamiento temporal.

    Args:
        meeting_id: Identificador de la asamblea.

    Returns:
        dict | None: Asamblea encontrada o None si no existe.
    """
    for m in MEETINGS:
        if m["id"] == meeting_id:
            return m
    return None


@router.post(
    "/",
    response_model=MeetingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva asamblea",
)
def create_meeting(
    payload: MeetingCreate,
    current_user: PublicUser = Depends(get_current_user),
):
    """Crea una asamblea en estado **pendiente**.

    Requiere rol **admin** (RB-01). Genera un identificador único (RD-07).

    Args:
        payload: Datos base (título, hora de inicio, quorum mínimo).
        current_user: Usuario autenticado.

    Raises:
        HTTPException: 403 si el usuario no es admin.

    Returns:
        MeetingOut: Asamblea creada.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el administrador puede crear asambleas.",
        )

    data = payload.model_dump()
    data.update(
        {
            "id": len(MEETINGS) + 1,
            "status": MeetingStatusEnum.pendiente.value,
            "created_at": datetime.utcnow(),
            "opened_at": None,
            "closed_at": None,
        }
    )
    MEETINGS.append(data)
    return MeetingOut(**data)


@router.get("/", response_model=List[MeetingOut], summary="Listar asambleas")
def list_meetings():
    """Lista todas las asambleas registradas.

    Raises:
        HTTPException: 404 si no hay asambleas registradas.

    Returns:
        list[MeetingOut]: Colección de asambleas.
    """
    if not MEETINGS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No hay asambleas registradas."
        )
    return [MeetingOut(**m) for m in MEETINGS]


@router.patch(
    "/{meeting_id}",
    response_model=MeetingOut,
    summary="Actualizar datos de una asamblea",
)
def update_meeting(
    meeting_id: int,
    payload: MeetingUpdate,
    current_user: PublicUser = Depends(get_current_user),
):
    """Actualiza metadatos de una asamblea (no cambia aperturas/cierres).

    Requiere rol **admin** (RB-01). Permite modificar título, hora y quorum.

    Args:
        meeting_id: Identificador de la asamblea.
        payload: Campos opcionales a actualizar.
        current_user: Usuario autenticado.

    Raises:
        HTTPException:
            403 si no es admin.
            404 si no existe la asamblea.

    Returns:
        MeetingOut: Asamblea actualizada.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el administrador puede actualizar asambleas.",
        )

    m = _get_meeting(meeting_id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Asamblea no encontrada."
        )

    updates = payload.model_dump(exclude_unset=True)
    # Validación de estado si viene en payload (no cambia aperturas/cierres aquí)
    if "status" in updates:
        status_val = (
            updates["status"].value if hasattr(updates["status"], "value") else updates["status"]
        )
        if status_val not in [e.value for e in MeetingStatusEnum]:
            raise HTTPException(status_code=400, detail="Estado inválido.")
        m["status"] = status_val
        updates.pop("status", None)

    for k, v in updates.items():
        m[k] = v

    return MeetingOut(**m)


@router.post("/open", summary="Abrir asamblea para votación")
def open_meeting(
    meeting_id: int = Query(..., description="ID de la asamblea a abrir"),
    current_user: PublicUser = Depends(get_current_user),
):
    """Transición **pendiente → abierta**.

    Requiere rol **admin** (RB-01). Valida que **no haya otra asamblea abierta**
    (RB-02).

    Args:
        meeting_id: Identificador de la asamblea a abrir.
        current_user: Usuario autenticado.

    Raises:
        HTTPException:
            403 si no es admin.
            409 si ya existe una asamblea abierta.
            404 si no existe la asamblea.
            400 si la asamblea no está en estado pendiente.

    Returns:
        dict: Mensaje y asamblea resultante.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el administrador puede abrir asambleas.",
        )

    # RB-02: no permitir dos asambleas abiertas simultáneamente
    for existing in MEETINGS:
        if existing["status"] == MeetingStatusEnum.abierta.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una asamblea abierta.",
            )

    m = _get_meeting(meeting_id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Asamblea no encontrada."
        )
    if m["status"] != MeetingStatusEnum.pendiente.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La asamblea no está pendiente."
        )

    m["status"] = MeetingStatusEnum.abierta.value
    m["opened_at"] = datetime.utcnow()
    return {"message": f"Asamblea '{m['title']}' abierta correctamente.", "meeting": MeetingOut(**m)}


@router.post("/close", summary="Cerrar asamblea en curso")
def close_meeting(
    meeting_id: int = Query(..., description="ID de la asamblea a cerrar"),
    current_user: PublicUser = Depends(get_current_user),
):
    """Transición **abierta → cerrada**.

    Requiere rol **admin** (RB-01).

    Args:
        meeting_id: Identificador de la asamblea a cerrar.
        current_user: Usuario autenticado.

    Raises:
        HTTPException:
            403 si no es admin.
            404 si no existe la asamblea.
            400 si la asamblea no está abierta.

    Returns:
        dict: Mensaje y asamblea resultante.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el administrador puede cerrar asambleas.",
        )

    m = _get_meeting(meeting_id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Asamblea no encontrada."
        )
    if m["status"] != MeetingStatusEnum.abierta.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La asamblea no está abierta."
        )

    m["status"] = MeetingStatusEnum.cerrada.value
    m["closed_at"] = datetime.utcnow()
    return {"message": f"Asamblea '{m['title']}' cerrada correctamente.", "meeting": MeetingOut(**m)}
