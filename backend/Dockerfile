# ============================================================
# Backend AgoraX - FastAPI + Poetry (Optimizado)
# ============================================================

FROM python:3.11-slim

# ------------------------------
# Configuración básica del entorno
# ------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Config global de Poetry
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# ------------------------------
# Dependencias del sistema
# ------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# ------------------------------
# Instalación de Poetry
# ------------------------------
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# ------------------------------
# Copiar solo archivos de dependencias para usar caché
# ------------------------------
COPY pyproject.toml ./
# Si en el futuro tienes poetry.lock, descomenta esto:
# COPY poetry.lock ./

# ------------------------------
# Instalación de dependencias (incluye grupo docs si lo defines)
# ------------------------------
RUN poetry install --no-root --no-ansi

# ------------------------------
# Copiar el código fuente de la app
# ------------------------------
COPY ./app /app/app

# ------------------------------
# Crear usuario no root para ejecutar la app
# ------------------------------
RUN useradd -m agorax
USER agorax

# ------------------------------
# Exponer puerto de FastAPI
# ------------------------------
EXPOSE 8000

# ------------------------------
# Comando por defecto
# ------------------------------
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
