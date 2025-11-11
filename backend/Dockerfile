# ============================================================
# 🐍 Backend AgoraX - FastAPI + Poetry
# ============================================================

FROM python:3.11-slim

# Configuración del entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Instalar Poetry (gestor de dependencias)
# ------------------------------------------------------------
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copiar solo archivos de dependencias para aprovechar cache
COPY pyproject.toml ./

# Instalar dependencias del proyecto SIN crear venv local
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Copiar el código fuente
COPY ./app /app/app

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
