"""
backend/app/schemas/vote_schema.py

Esquemas Pydantic relacionados con votos (Vote).

Incluye:
- Entrada de voto (VoteCreate).
- Respuesta al registrar un voto (VoteResponse).
- Agregaciones de resultados para visualización (VoteAggregate).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VoteCreate(BaseModel):
    """
    Esquema de entrada para registrar un voto.

    Implementa varias reglas:
    - RD-01: un propietario solo puede votar una vez por punto.
    - RD-03: el usuario debe estar autenticado (se verifica en seguridad).
    - RB-03: se asume que ya confirmó asistencia.
    """

    agenda_item_id: int
    value: str = Field(..., description="Opción de voto en texto claro (antes de cifrado).")
    ip_address: Optional[str] = Field(
        None,
        description="Dirección IP desde la que se registra el voto (para auditoría).",
    )


class VoteResponse(BaseModel):
    """
    Esquema de salida tras registrar un voto.

    No expone el valor cifrado, solo confirma el registro y contexto.
    """

    id: int
    agenda_item_id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class VoteAggregate(BaseModel):
    """
    Esquema para representar resultados agregados de votación.

    Por ejemplo, para gráficos o reportes en el frontend.
    """

    agenda_item_id: int
    option: str
    total_votos: int
    porcentaje: float
