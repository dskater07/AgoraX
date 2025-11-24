"""
backend/app/core/config.py

Configuración central de la aplicación AgoraX.
"""

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de entorno para AgoraX.
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

    TOTAL_PROPIETARIOS: int = 100
    QUORUM_MIN: float = 51.0

    VOTE_ENCRYPTION_KEY: str | None = None  # Si no se define, se genera al vuelo (solo dev)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Devuelve una instancia singleton de Settings.
    """
    return Settings()
