from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .auth import get_current_user, PublicUser

router = APIRouter()

# ================================
# Modelos
# ================================
class Meeting(BaseModel):
    title: str
    start_time: datetime
    quorum_min: Optional[float] = 51.0

class MeetingResponse(Meeting):
    id: int
    status: str
    created_at: datetime
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None


# ================================
# "Base de datos" temporal
# ================================
MEETINGS: List[dict] = []


# ================================
# Endpoints
# ================================
@router.post("/", response_model=MeetingResponse, summary="Crear nueva asamblea")
def create_meeting(meeting: Meeting, current_user: PublicUser = Depends(get_current_user)):
    """
    Crea una asamblea en estado 'pendiente'.
    En la versión final, solo administradores podrán hacerlo.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el administrador puede crear asambleas.")
    
    meeting_data = meeting.dict()
    meeting_data["id"] = len(MEETINGS) + 1
    meeting_data["status"] = "pendiente"
    meeting_data["created_at"] = datetime.utcnow()
    meeting_data["opened_at"] = None
    meeting_data["closed_at"] = None
    MEETINGS.append(meeting_data)
    return meeting_data


@router.get("/", response_model=List[MeetingResponse], summary="Listar asambleas creadas")
def list_meetings():
    """
    Retorna la lista de asambleas existentes.
    """
    if not MEETINGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay asambleas registradas.")
    return MEETINGS


@router.post("/open", summary="Abrir asamblea para votación")
def open_meeting(
    meeting_id: int = Query(..., description="ID de la asamblea a abrir"),
    current_user: PublicUser = Depends(get_current_user),
):
    """
    Cambia el estado de 'pendiente' a 'abierta'.
    RB-01: Solo el administrador puede abrir votaciones.
    RB-02: Debe cerrarse un punto antes de abrir otro.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el administrador puede abrir asambleas.")

    for m in MEETINGS:
        if m["status"] == "abierta":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe una asamblea abierta.")
    for m in MEETINGS:
        if m["id"] == meeting_id:
            if m["status"] != "pendiente":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La asamblea no está pendiente.")
            m["status"] = "abierta"
            m["opened_at"] = datetime.utcnow()
            return {"message": f"Asamblea '{m['title']}' abierta correctamente.", "meeting": m}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asamblea no encontrada.")


@router.post("/close", summary="Cerrar asamblea en curso")
def close_meeting(
    meeting_id: int = Query(..., description="ID de la asamblea a cerrar"),
    current_user: PublicUser = Depends(get_current_user),
):
    """
    Cambia el estado de 'abierta' a 'cerrada'.
    RB-01: Solo el administrador puede cerrar votaciones.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el administrador puede cerrar asambleas.")
    for m in MEETINGS:
        if m["id"] == meeting_id:
            if m["status"] != "abierta":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La asamblea no está abierta.")
            m["status"] = "cerrada"
            m["closed_at"] = datetime.utcnow()
            return {"message": f"Asamblea '{m['title']}' cerrada correctamente.", "meeting": m}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asamblea no encontrada.")
