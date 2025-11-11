from fastapi import APIRouter, HTTPException, Depends, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional
import os

router = APIRouter()

# ================================
# Configuración JWT
# ================================
JWT_SECRET: str = os.getenv("JWT_SECRET", "secret123")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# Seguridad de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)

# ================================
# Modelos Pydantic
# ================================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime

class PublicUser(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "propietario"

# ================================
# Simulación mínima de usuarios
# Reemplaza esto por consulta a BD.
# ================================
_DEMO_USER_DB = {
    # password plano: "admin"
    "admin@agorax.com": {
        "email": "admin@agorax.com",
        "full_name": "Administrador AgoraX",
        "role": "admin",
        "password_hash": pwd_context.hash("admin"),
        "is_active": True,
    }
}

def get_user_by_email(email: str) -> Optional[dict]:
    """
    Sustituir por SELECT a PostgreSQL.
    """
    return _DEMO_USER_DB.get(email)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(plain: str) -> str:
    return pwd_context.hash(plain)

def create_access_token(sub: str, expires_minutes: int = JWT_EXPIRE_MINUTES) -> dict:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"token": token, "expires_at": exp}

# ================================
# Dependencia: usuario actual
# ================================
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> PublicUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales no provistas")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    user = get_user_by_email(email)
    if not user or not user.get("is_active", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autorizado")

    return PublicUser(email=user["email"], full_name=user.get("full_name"), role=user.get("role", "propietario"))

# ================================
# Endpoints
# ================================
@router.post("/login", response_model=TokenResponse, summary="Autenticación y emisión de JWT")
def login(request: LoginRequest):
    user = get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token_data = create_access_token(sub=user["email"])
    return {
        "access_token": token_data["token"],
        "token_type": "bearer",
        "expires_at": token_data["expires_at"],
    }

@router.get("/me", response_model=PublicUser, summary="Información del usuario autenticado")
def me(current: PublicUser = Depends(get_current_user)):
    return current
