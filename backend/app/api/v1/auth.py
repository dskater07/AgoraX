"""
Módulo de Autenticación y Gestión de Sesiones (API v1)
------------------------------------------------------

Este módulo maneja el proceso de autenticación del sistema AgoraX,
incluyendo generación de tokens JWT, validación de identidad y
obtención de información del usuario autenticado.

Basado en FastAPI, Pydantic y Python-JOSE.

Reglas de negocio aplicadas:
    - RD-03: Solo usuarios autenticados pueden votar.
    - RB-01: Solo el administrador puede abrir o cerrar votaciones.
    - RB-06: Registrar información del acceso para auditoría.
"""

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


class LoginRequest(BaseModel):
    """Estructura de datos para solicitud de autenticación."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Respuesta generada tras autenticación exitosa."""
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class PublicUser(BaseModel):
    """Representación mínima del usuario autenticado en el sistema."""
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "propietario"


# -------------------------------------------------------------------
# Base de datos temporal para demostración (mock de usuarios)
# -------------------------------------------------------------------
_DEMO_USER_DB = {
    "admin@agorax.com": {
        "email": "admin@agorax.com",
        "full_name": "Administrador AgoraX",
        "role": "admin",
        "password_hash": get_password_hash("admin"),
        "is_active": True,
    }
}


def get_user_by_email(email: str) -> Optional[dict]:
    """
    Recupera un usuario de la base de datos temporal.

    Args:
        email: Dirección de correo del usuario.

    Returns:
        dict | None: Información del usuario o None si no existe.
    """
    return _DEMO_USER_DB.get(email)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> PublicUser:
    """
    Decodifica el token JWT y retorna los datos del usuario autenticado.

    Args:
        credentials: Credenciales HTTP Bearer proporcionadas por el cliente.

    Raises:
        HTTPException: Si el token no es válido, expiró o el usuario no existe.

    Returns:
        PublicUser: Modelo con información básica del usuario autenticado.
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


@router.post("/login", response_model=TokenResponse, summary="Autenticación y emisión de JWT")
def login(request: LoginRequest):
    """
    Realiza la autenticación del usuario y emite un token JWT firmado.

    Este endpoint valida las credenciales proporcionadas y, en caso de éxito,
    devuelve un token que permite realizar operaciones protegidas por seguridad.

    Args:
        request: Cuerpo de la solicitud con `email` y `password`.

    Raises:
        HTTPException: Si las credenciales son inválidas.

    Returns:
        TokenResponse: Token de acceso y metadatos de expiración.
    """
    user = get_user_by_email(request.email)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token, exp = create_access_token(user["email"])
    return {"access_token": token, "token_type": "bearer", "expires_at": exp}


@router.get("/me", response_model=PublicUser, summary="Información del usuario autenticado")
def me(current: PublicUser = Depends(get_current_user)):
    """
    Devuelve los datos del usuario autenticado actual.

    Args:
        current: Usuario autenticado obtenido desde el token.

    Returns:
        PublicUser: Información básica del usuario activo.
    """
    return current
