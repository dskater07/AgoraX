# ============================================================
# Backend AgoraX - FastAPI + Poetry
# ============================================================

FROM python:3.11-slim

# Evitar archivos .pyc y forzar logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias de sistema necesarias para psycopg2 y compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    ca-certificates \  # <--- Asegura certificados para HTTPS/SSL
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copiar definición de dependencias
COPY pyproject.toml ./

# Instalar dependencias declaradas (sin crear venv)
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Copiar código fuente de la app
COPY ./app /app/app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
