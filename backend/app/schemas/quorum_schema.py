"""
backend/app/schemas/quorum_schema.py

Esquemas Pydantic relacionados con el cálculo y visualización del quórum.

Estos esquemas soportan los endpoints expuestos en:
- api/v1/quorum.py
y la lógica implementada en:
- services/quorum_service.py
"""

from typing import List

from pydantic import BaseModel, Field


class QuorumStatus(BaseModel):
    """
    Resumen del estado de quórum de una asamblea.

    Campos:
        meeting_id: ID de la asamblea.
        presentes_coeficiente: Suma de coeficientes de los presentes.
        coeficiente_total: Suma total de coeficientes del conjunto.
        porcentaje_quorum: Porcentaje actual de quórum.
        cumple_quorum: Indica si se cumple el mínimo exigido.
    """

    meeting_id: int
    presentes_coeficiente: float = Field(..., description="Suma de coeficientes de presentes.")
    coeficiente_total: float = Field(..., description="Coeficiente total del conjunto.")
    porcentaje_quorum: float = Field(..., description="Porcentaje actual de quórum.")
    cumple_quorum: bool = Field(..., description="True si el quórum mínimo está cumplido.")


class QuorumDetail(BaseModel):
    """
    Detalle de quórum por asamblea.

    Incluye:
        status: resumen global del quórum.
        presentes: lista simplificada de presencias contribuyentes.
    """

    status: QuorumStatus
    presentes: List[dict]
