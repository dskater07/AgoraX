from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

# ============================================================
# CONFIGURACIÓN Y VARIABLES DE ENTORNO
# ============================================================
POSTGRES_USER = os.getenv("POSTGRES_USER", "agx_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "agx_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "agorax_db")
JWT_SECRET = os.getenv("JWT_SECRET", "secret123")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ============================================================
# CONEXIÓN A BASE DE DATOS
# ============================================================
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================================
# CONFIGURACIÓN FASTAPI
# ============================================================
app = FastAPI(
    title="AgoraX Backend API",
    description="Sistema de votación electrónica para asambleas residenciales - Proyecto ITM (Calidad del Software)",
    version="1.0.0"
)

# CORS para desarrollo (permitir frontend)
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELOS BÁSICOS Pydantic
# ============================================================
class User(BaseModel):
    email: str
    password: str

class Vote(BaseModel):
    meeting_id: int
    vote_option: str

# Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================================================
# DEPENDENCIA DE SESIÓN DB
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================
# ENDPOINT DE SALUD
# ============================================================
@app.get("/health", tags=["system"])
def health_check():
    """
    Verifica el estado general del backend y la conexión a la base de datos.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "timestamp": datetime.utcnow()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================
# AUTENTICACIÓN SIMPLIFICADA (JWT)
# ============================================================
@app.post("/auth/login", tags=["auth"])
def login(user: User):
    """
    Autenticación básica con JWT (solo demostrativo).
    """
    if user.email == "admin@agorax.com" and user.password == "admin":
        payload = {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

# ============================================================
# ENDPOINTS DE VOTACIÓN
# ============================================================
@app.post("/votes", tags=["votes"])
def create_vote(vote: Vote):
    """
    Endpoint simulado para registrar un voto.
    """
    # En producción: validar token JWT, estado de reunión y quorum.
    return {
        "message": "Voto registrado correctamente",
        "meeting_id": vote.meeting_id,
        "vote_option": vote.vote_option,
        "timestamp": datetime.utcnow()
    }

@app.get("/votes", tags=["votes"])
def list_votes():
    """
    Devuelve una lista simulada de votos.
    """
    # En entorno real, esto se consultaría desde PostgreSQL.
    return [
        {"user_id": 1, "meeting_id": 1, "vote_option": "Sí"},
        {"user_id": 2, "meeting_id": 1, "vote_option": "No"}
    ]

# ============================================================
# ENDPOINTS DE REGLAS DE NEGOCIO
# ============================================================
@app.get("/rules", tags=["rules"])
def list_rules():
    """
    Devuelve todas las reglas de negocio (RD, RB, RI).
    """
    return {
        "definicionales": [
            "RD-01: Un propietario solo puede votar una vez por cada punto.",
            "RD-02: Un apoderado representa máximo a un propietario.",
            "RD-03: Solo los usuarios autenticados pueden votar.",
            "RD-04: El quorum mínimo es del 51%.",
            "RD-05: Los resultados no pueden modificarse tras el cierre."
        ],
        "comportamiento": [
            "RB-01: Solo el administrador puede abrir o cerrar votaciones.",
            "RB-02: Debe cerrarse un punto antes de abrir otro.",
            "RB-03: El usuario debe confirmar asistencia antes de votar.",
            "RB-04: El sistema notifica apertura/cierre a todos los usuarios.",
            "RB-05: Los votos no pueden modificarse una vez emitidos."
        ],
        "implícitas": [
            "RI-01: Las reglas deben almacenarse en un repositorio central.",
            "RI-02: Cambios a reglas requieren aprobación formal.",
            "RI-03: Se debe mantener un glosario del sistema."
        ]
    }

# ============================================================
# ROOT - HOME
# ============================================================
@app.get("/", tags=["system"])
def home():
    """
    Página inicial de referencia.
    """
    return {
        "project": "AgoraX",
        "version": "1.0.0",
        "message": "Bienvenido al backend de AgoraX - Sistema de votación electrónica (ITM)."
    }
