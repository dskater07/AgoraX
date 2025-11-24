"""
backend/app/services/__init__.py

Paquete de servicios de AgoraX.

Los servicios encapsulan lógica de negocio reutilizable,
como auditoría, cálculo de quórum y evaluación de reglas.
Este archivo solo expone los submódulos sin importar clases
directamente, para evitar ciclos de dependencia y mantener
una arquitectura limpia y modular.
"""

__all__ = [
    "audit_service",
    "quorum_service",
    "rule_engine",
]
