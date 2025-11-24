"""
backend/app/core/security.py

Seguridad: hashing de contraseñas, JWT, usuario actual,
y cifrado de votos (RD-06).
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import SessionLocal
from app.models import models

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ================= JWT ==================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña en texto plano contra su hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera el hash seguro de una contraseña.
    """
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    """
    Crea un JWT para el usuario autenticado.

    :param subject: Identificador (email) del usuario.
    :param expires_minutes: Minutos de expiración.
    """
    if expires_minutes is None:
        expires_minutes = settings.JWT_EXPIRE_MINUTES

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def get_db_for_security():
    """
    Sesión de BD exclusiva para funciones de seguridad.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_for_security),
) -> models.User:
    """
    Obtiene el usuario actual a partir del JWT (RD-03).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise credentials_exception
    return user

# ================= CIFRADO DE VOTOS (RD-06) ==================

# Si viene de entorno, usamos esa clave, si no generamos una solo para dev.
if settings.VOTE_ENCRYPTION_KEY:
    _key = settings.VOTE_ENCRYPTION_KEY.encode("utf-8")
else:
    _key = Fernet.generate_key()

_fernet = Fernet(_key)


def encrypt_vote_value(value: str) -> str:
    """
    Cifra el valor del voto antes de almacenarlo (RD-06).

    :param value: Opción de voto en claro (Sí/No/Abstención).
    :return: Cadena cifrada base64.
    """
    token = _fernet.encrypt(value.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_vote_value(value_encrypted: str) -> str:
    """
    Descifra el valor del voto (para agregación, nunca para mostrar individualmente).

    :param value_encrypted: Cadena cifrada almacenada.
    :return: Valor en claro.
    """
    return _fernet.decrypt(value_encrypted.encode("utf-8")).decode("utf-8")
