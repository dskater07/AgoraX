from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .auth import get_current_user, PublicUser

router = APIRouter()

# ================================
# Modelo de datos Pydantic
# ================================
class Vote(BaseModel):
    meeting_id: int
    vote_option: str

class VoteResponse(Vote):
    user_email: str
    timestamp: datetime

# ================================
# "Base de datos" temporal
# ================================
VOTE_DB: List[dict] = []

# ================================
# Endpoints
# ================================
@router.post("/", response_model=VoteResponse, summary="Registrar un voto")
def create_vote(vote: Vote, current_user: PublicUser = Depends(get_current_user)):
    """
    Registra un voto emitido por un usuario autenticado.
    Luego se reemplazará por inserción real en PostgreSQL.
    """
    # Validación simple de voto duplicado
    for existing_vote in VOTE_DB:
        if (
            existing_vote["meeting_id"] == vote.meeting_id
            and existing_vote["user_email"] == current_user.email
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un voto de este usuario en este punto."
            )

    vote_record = {
        "meeting_id": vote.meeting_id,
        "vote_option": vote.vote_option,
        "user_email": current_user.email,
        "timestamp": datetime.utcnow(),
    }
    VOTE_DB.append(vote_record)
    return vote_record


@router.get("/", response_model=List[VoteResponse], summary="Listar votos emitidos")
def list_votes(current_user: PublicUser = Depends(get_current_user)):
    """
    Lista los votos registrados (demo en memoria).
    En producción filtrará por reunión y usuario.
    """
    if not VOTE_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay votos registrados.")
    return VOTE_DB


@router.delete("/{meeting_id}", summary="Eliminar voto de un usuario (demo)")
def delete_vote(meeting_id: int, current_user: PublicUser = Depends(get_current_user)):
    """
    Permite eliminar un voto emitido, solo para pruebas.
    En versión real no debe existir (los votos son inmutables).
    """
    global VOTE_DB
    before = len(VOTE_DB)
    VOTE_DB = [v for v in VOTE_DB if not (v["meeting_id"] == meeting_id and v["user_email"] == current_user.email)]
    if len(VOTE_DB) == before:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró voto para eliminar.")
    return {"message": "Voto eliminado (solo modo demo)."}
