"""
Módulo de Votaciones (API v1)
-----------------------------

Gestiona el registro y la consulta de votos emitidos en AgoraX.
Implementación inicial *in-memory* (para demo); lista para
migrarse a PostgreSQL sin cambiar la interfaz pública.

Reglas de negocio aplicadas:
    - RD-01: Un propietario solo puede votar una vez por cada punto.
    - RD-03: Solo usuarios autenticados pueden votar.
    - RD-05 / RB-05: Los votos no son editables tras emitirse.
    - RB-06: (Preparado) Registrar IP, fecha y hora de cada voto.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from .auth import PublicUser, get_current_user
from app.schemas.vote_schema import VoteCreate, VoteOut

router = APIRouter()

# -------------------------------------------------------------------
# Almacenamiento temporal (mock). Reemplazar por persistencia real.
# -------------------------------------------------------------------
VOTE_DB: list[dict] = []


def _find_user_vote(meeting_id: int, email: str) -> dict | None:
    """Busca el voto de un usuario para un punto específico.

    Args:
        meeting_id: Identificador de la asamblea/punto sometido a votación.
        email: Correo del usuario autenticado.

    Returns:
        dict | None: Registro de voto si existe, en caso contrario None.
    """
    for v in VOTE_DB:
        if v["meeting_id"] == meeting_id and v["user_email"] == email:
            return v
    return None


@router.post("/", response_model=VoteOut, status_code=status.HTTP_201_CREATED, summary="Registrar un voto")
def create_vote(
    payload: VoteCreate,
    request: Request,
    current_user: PublicUser = Depends(get_current_user),
):
    """Registra un voto para el usuario autenticado.

    Valida la regla **RD-01** para impedir votos duplicados por usuario y
    punto de la asamblea. Guarda IP y marca de tiempo (RB-06 listo).

    Args:
        payload: Cuerpo con `meeting_id` y `vote_option` (Sí/No/Abstención).
        request: Objeto de petición para obtener IP del cliente.
        current_user: Usuario autenticado inyectado por dependencia.

    Raises:
        HTTPException: 400 si el usuario ya votó en ese punto.

    Returns:
        VoteOut: Representación del voto recién creado.
    """
    # RD-01: un voto por usuario/punto
    if _find_user_vote(payload.meeting_id, current_user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un voto de este usuario en este punto.",
        )

    client_ip = request.client.host if request.client else None

    record = {
        "id": len(VOTE_DB) + 1,
        "meeting_id": payload.meeting_id,
        "user_id": None,                     # se completará al integrar BD
        "user_email": current_user.email,
        "vote_option": payload.vote_option.value,  # Enum -> str
        "ip_address": client_ip,
        "timestamp": datetime.utcnow(),
    }
    VOTE_DB.append(record)
    return VoteOut(**record)


@router.get("/", response_model=List[VoteOut], summary="Listar votos emitidos")
def list_votes(current_user: PublicUser = Depends(get_current_user)):
    """Lista los votos registrados (modo demostración).

    En la versión con persistencia real, este endpoint podrá:
      - Filtrar por `meeting_id` y/o usuario.
      - Limitar visibilidad por rol (admin/revisor).

    Args:
        current_user: Usuario autenticado inyectado por dependencia.

    Raises:
        HTTPException: 404 si aún no hay votos.

    Returns:
        list[VoteOut]: Colección de votos.
    """
    if not VOTE_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay votos registrados.",
        )
    return [VoteOut(**v) for v in VOTE_DB]


@router.delete(
    "/{meeting_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar voto del usuario (solo DEMO)",
)
def delete_vote(meeting_id: int, current_user: PublicUser = Depends(get_current_user)):
    """Elimina el voto del usuario en un punto (solo para pruebas).

    **Nota:** En producción esta operación no debe existir (RD-05 / RB-05).
    Se mantiene en modo demo para facilitar pruebas manuales durante el
    desarrollo y la validación funcional.

    Args:
        meeting_id: Identificador del punto/asamblea.
        current_user: Usuario autenticado inyectado por dependencia.

    Raises:
        HTTPException: 404 si no se encontró un voto del usuario para ese punto.

    Returns:
        dict: Mensaje de confirmación.
    """
    global VOTE_DB
    before = len(VOTE_DB)
    VOTE_DB = [
        v
        for v in VOTE_DB
        if not (v["meeting_id"] == meeting_id and v["user_email"] == current_user.email)
    ]
    if len(VOTE_DB) == before:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró voto para eliminar.",
        )
    return {"message": "Voto eliminado (solo modo demo)."}
