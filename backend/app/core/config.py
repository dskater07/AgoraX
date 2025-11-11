import os
from functools import lru_cache

class Settings:
    # --- App ---
    APP_NAME: str = os.getenv("APP_NAME", "AgoraX Backend API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_DESC: str = os.getenv(
        "APP_DESC",
        "Sistema de votación electrónica para asambleas residenciales - Proyecto ITM (Calidad del Software)"
    )

    # --- DB ---
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "agx_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "agx_pass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "agorax_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL: str = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # --- Security / JWT ---
    JWT_SECRET: str = os.getenv("JWT_SECRET", "secret123")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # --- CORS ---
    CORS_ORIGINS: list[str] = [
        o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    ]

    # --- Business params (quorum, etc) ---
    TOTAL_PROPIETARIOS: int = int(os.getenv("TOTAL_PROPIETARIOS", "100"))
    QUORUM_MIN: float = float(os.getenv("QUORUM_MIN", "51.0"))

@lru_cache
def get_settings() -> Settings:
    return Settings()
