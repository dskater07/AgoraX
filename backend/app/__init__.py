"""
backend/app/__init__.py

Inicializador del paquete principal de AgoraX.

Este módulo define únicamente los subpaquetes disponibles
y evita realizar importaciones profundas para prevenir ciclos
de dependencias y errores de carga en tiempo de ejecución.
"""

__all__ = [
    "api",
    "core",
    "models",
    "schemas",
    "services",
]
