# AgoraX – Sistema de Votación Electrónica  
Guía oficial de despliegue en entornos locales, Docker y producción  
Proyecto académico – Calidad del Software – ITM

---

# 🔧 1. Prerrequisitos

Para ejecutar AgoraX necesitas:

| Software | Versión recomendada | Uso |
|----------|----------------------|-----|
| **Docker Desktop** | 4.x o superior | Contenedores backend/BD |
| **Docker Compose v2** | Integrado a Docker Desktop | Orquestación |
| **Git** | Última versión | Clonar o actualizar repositorio |
| **Navegador moderno** | Chrome / Edge / Firefox | Acceso a Swagger/Redoc |

---

# 📁 2. Estructura del proyecto

```
AgoraX/
│── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── app/
│       ├── main.py
│       ├── api/
│       │   └── v1/
│       │       ├── auth.py
│       │       ├── meetings.py
│       │       ├── quorum.py
│       │       ├── votes.py
│       │       └── rules.py
│       ├── core/
│       ├── models/
│       └── schemas/
│
│── db/
│   └── init.sql
│
│── docker-compose.yml
│── .env
│── README.md
│── README_DEPLOY.md
```

---

# 🔐 3. Configuración de variables (.env)

Debe existir un archivo `.env` en la raíz:

```
POSTGRES_USER=agx_user
POSTGRES_PASSWORD=agx_pass
POSTGRES_DB=agorax_db

JWT_SECRET=secret123
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

TOTAL_PROPIETARIOS=100
QUORUM_MIN=51.0
```

Si no existe:

```bash
nano .env
```

---

# 🐳 4. Despliegue usando Docker Compose

En la raíz del proyecto:

```bash
docker compose up -d --build
```

Servicios levantados:

| Servicio | Descripción |
|----------|-------------|
| **agorax-backend** | API FastAPI |
| **agorax-db** | PostgreSQL 17 |

*(Redis, gateway y monitorización son opcionales.)*

---

# 🔎 5. Verificar funcionamiento

## 5.1 Contenedores activos

```bash
docker compose ps
```

Salida esperada:

```
agorax-backend   Up    0.0.0.0:8000->8000/tcp
agorax-db        Up    0.0.0.0:5433->5432/tcp
```

## 5.2 Logs del backend

```bash
docker logs -f agorax-backend
```

---

# 🌐 6. Probar el backend

## 6.1 Healthcheck

```bash
curl http://localhost:8000/health
```

Debe responder:

```json
{"status":"ok","database":"connected"}
```

## 6.2 Swagger (documentación interactiva)

👉 `http://localhost:8000/docs`

## 6.3 ReDoc

👉 `http://localhost:8000/redoc`

*(Si aparece en blanco, el navegador está bloqueando JS CDN.)*

---

# 🧪 7. Pruebas funcionales de API

## 7.1 Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@agorax.com","password":"admin"}'
```

Guardar token:

```bash
TOKEN="TU_TOKEN_AQUI"
```

## 7.2 Crear asamblea

```bash
curl -X POST http://localhost:8000/api/v1/meetings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Asamblea Ordinaria 2025"}'
```

## 7.3 Registrar presencia

```bash
curl -X POST "http://localhost:8000/api/v1/quorum/presence?meeting_id=1" \
  -H "Authorization: Bearer $TOKEN"
```

## 7.4 Emitir voto

```bash
curl -X POST http://localhost:8000/api/v1/votes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"meeting_id":1,"vote_option":"Sí"}'
```

---

# 📦 8. Administración

| Acción | Comando |
|--------|---------|
| Detener servicios | `docker compose down` |
| Detener + eliminar volúmenes | `docker compose down -v` |
| Reconstruir | `docker compose up -d --build` |
| Ver logs | `docker logs -f agorax-backend` |
| Entrar al contenedor | `docker exec -it agorax-backend bash` |
| Entrar a PostgreSQL | `docker exec -it agorax-db psql -U agx_user -d agorax_db` |

---

# 📘 9. Documentación técnica (MkDocs)

Si se habilitan en `pyproject.toml`:

```bash
docker compose run --rm backend poetry run mkdocs serve -a 0.0.0.0:8080
```

Documentación disponible en:

👉 `http://localhost:8080`

---

# 📡 10. Añadir Redis (opcional)

En docker-compose:

```yaml
redis:
  image: redis:7
  ports:
    - "6379:6379"
  networks:
    - agorax-net
```

---

# 🔌 11. Gateway Node.js + Socket.io (opcional)

Añadir:

```
gateway/server.js
gateway/Dockerfile
```

Y en compose:

```yaml
gateway:
  build: ./gateway
  ports:
    - "9000:9000"
  depends_on:
    - backend
    - redis
```

---

# 📊 12. Monitorización (Prometheus + Grafana)

### En docker-compose.yml:

```yaml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

### En FastAPI:

```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

---

# 🔐 13. Seguridad recomendada

- HTTPS con Nginx reverse proxy  
- Rotación de claves JWT  
- Cifrado AES-256 para votos  
- Registro de auditoría (IP, timestamp, UA)  

---

# ☁️ 14. Deploy en Producción

1. Instalar Docker en el servidor  
2. Clonar el proyecto:

```bash
git clone https://github.com/tu-org/agorax.git
cd agorax
```

3. Ejecutar:

```bash
docker compose up -d --build
```

4. Configurar Nginx + HTTPS (Certbot)  

---

# 👥 15. Autores

Proyecto académico – **Calidad del Software – ITM (2025-2)**

- **Gaviria Ocampo, Johan Esteban**  
- **Patiño Montoya, Damián**  
- **Velilla Flórez, Luisa Fernanda**

Director académico:  
**Alex Mauricio Pérez – Facultad de Ingenierías – ITM**

