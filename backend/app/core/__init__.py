"""
Módulo Core de AgoraX
---------------------

Este paquete contiene los componentes internos y transversales del sistema,
responsables de proporcionar configuración, seguridad y utilidades base para
toda la capa de API y lógica de negocio.

Submódulos principales:
    - config.py:
        Maneja configuración centralizada del sistema a través de
        variables de entorno y parámetros de negocio (quórum, JWT,
        credenciales de BD, etc).

    - security.py:
        Implementa funciones criptográficas, hashing de contraseñas
        (bcrypt), generación y validación de tokens JWT y utilidades
        relacionadas con identidad y autenticación.

El propósito del paquete `core` es aislar la infraestructura y los servicios
de soporte que no pertenecen a un dominio funcional específico, permitiendo
una arquitectura más ordenada, testeable y mantenible.
"""

__all__ = ["config", "security"]
