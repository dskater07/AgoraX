"""
backend/app/api/v1/quorum.py

Endpoints para consultar el estado de quórum de una asamblea.

Utiliza el servicio:
- services/quorum_service.py

Y los esquemas:
- QuorumStatus
- QuorumDetail
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import get_current_user
from app.models import Meeting, User
from app.schemas.quorum_schema import QuorumDetail
from app.services.quorum_service import calculate_quorum

router = APIRouter(prefix="/api/v1/quorum", tags=["quorum"])


@router.get("/{meeting_id}", response_model=QuorumDetail)
def get_quorum(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve el detalle del quórum actual de la asamblea.

    Incluye:
        - Porcentaje de quórum.
        - Si cumple el mínimo.
        - Lista de presentes y sus coeficientes.
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asamblea no encontrada.",
        )

    detail = calculate_quorum(db, meeting_id=meeting_id)
    return detail
