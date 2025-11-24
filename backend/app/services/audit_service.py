"""
backend/app/services/audit_service.py

Servicio de auditoría para AgoraX.

Este módulo centraliza la creación y consulta de registros de auditoría (AuditLog),
de forma que cualquier acción relevante en el sistema pueda ser trazada.

Reglas de negocio relacionadas:
- RD-09: El acta debe incluir quórum, votos y evidencia de decisiones.
- RB-06: Registrar IP, fecha y hora de cada voto (complementado con AuditLog).
"""

from typing import Optional, List

from sqlalchemy.orm import Session

from app.models import AuditLog


def log_action(
    db: Session,
    *,
    user_id: Optional[int],
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    description: Optional[str] = None,
) -> AuditLog:
    """
    Registra una acción en la tabla de auditoría.

    Parámetros:
        db: Sesión de base de datos.
        user_id: ID del usuario que ejecuta la acción (puede ser None).
        action: Código o etiqueta de la acción (ej. 'CAST_VOTE').
        entity_type: Tipo de entidad afectada (ej. 'Meeting', 'Vote').
        entity_id: Identificador de la entidad afectada (si aplica).
        description: Descripción opcional con más contexto.

    Retorna:
        El objeto AuditLog persistido.

    Ejemplos típicos de uso:
        - Al registrar un voto.
        - Al abrir o cerrar una votación.
        - Al cambiar el estado de una asamblea.
    """
    audit = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


def get_audit_for_entity(
    db: Session,
    *,
    entity_type: str,
    entity_id: int,
    limit: int = 50,
) -> List[AuditLog]:
    """
    Obtiene los últimos registros de auditoría asociados a una entidad concreta.

    Parámetros:
        db: Sesión de base de datos.
        entity_type: Tipo de entidad (ej. 'Meeting', 'Vote').
        entity_id: ID de la entidad.
        limit: Número máximo de registros a devolver.

    Retorna:
        Lista de objetos AuditLog ordenados por fecha descendente.
    """
    return (
        db.query(AuditLog)
        .filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id,
        )
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )
