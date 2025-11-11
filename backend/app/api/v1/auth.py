from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from jose import JWTError

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
)
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()
security = HTTPBearer(auto_error=False)

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
# (para cuando no hay BD conectada)
# ================================
_DEMO_USER_DB = {
    "admin@agorax.com": {
        "email": "admin@agorax.com",
        "full_name": "Administrador AgoraX",
        "role": "admin",
        "password_hash": get_password_hash("admin"),  # 🔒 se genera con bcrypt
        "is_active": True,
    }
}

def get_user_by_email(email: str) -> Optional[dict]:
    """
    Sustituir por SELECT real en PostgreSQL.
    """
    return _DEMO_USER_DB.get(email)

# ================================
# Dependencia de usuario actual
# ================================
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> PublicUser:
    """
    Decodifica el JWT y devuelve el usuario autenticado.
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no proporcionado")

    token = credentials.credentials
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    user = get_user_by_email(email)
    if not user or not user.get("is_active"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autorizado")

    return PublicUser(email=user["email"], full_name=user.get("full_name"), role=user.get("role", "propietario"))

# ================================
# Endpoints
# ================================
@router.post("/login", response_model=TokenResponse, summary="Autenticación y emisión de JWT")
def login(request: LoginRequest):
    """
    Autentica un usuario (demo) y genera un JWT firmado.
    """
    user = get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token, exp = create_access_token(user["email"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": exp,
    }

@router.get("/me", response_model=PublicUser, summary="Información del usuario autenticado")
def me(current: PublicUser = Depends(get_current_user)):
    """Devuelve los datos del usuario autenticado."""
    return current
