"""
backend/app/core/config.py

Módulo de configuración central de AgoraX.

Utiliza Pydantic Settings para leer variables desde el entorno (.env),
lo que permite una configuración clara y trazable del backend.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración general del backend AgoraX.

    Atributos principales:
        APP_NAME: Nombre visible de la API.
        APP_VERSION: Versión del backend.
        POSTGRES_*: Parámetros de conexión a PostgreSQL.
        JWT_*: Configuración de tokens JWT.
        QUORUM_MIN: Umbral mínimo de quórum.
        VOTE_ENCRYPTION_KEY: Clave opcional para cifrar votos.
    """

    APP_NAME: str = "AgoraX Backend API"
    APP_VERSION: str = "1.0.0"

    POSTGRES_USER: str = "agx_user"
    POSTGRES_PASSWORD: str = "agx_pass"
    POSTGRES_DB: str = "agorax_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    JWT_SECRET: str = "secret123"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    QUORUM_MIN: float = 51.0

    VOTE_ENCRYPTION_KEY: str | None = None

    class Config:
        """
        Configuración de Pydantic Settings:

        - Lee variables desde el archivo .env si existe.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Devuelve una instancia única de Settings (patrón singleton simple).

    Esta función se usa en todo el backend para acceder a la configuración
    sin recrear el objeto en cada import.
    """
    return Settings()
