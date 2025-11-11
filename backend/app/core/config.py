import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "agx_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "agx_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "agorax_db")
JWT_SECRET = os.getenv("JWT_SECRET", "secret123")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
