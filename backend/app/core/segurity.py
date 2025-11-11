from datetime import datetime, timedelta, timezone
from typing import Tuple, Any, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import get_settings

# Hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str) -> Tuple[str, datetime]:
    """
    Crea un JWT usando configuración centralizada.
    Retorna (token, expires_at).
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, exp

def decode_token(token: str) -> dict:
    """
    Decodifica un JWT y devuelve el payload.
    Lanza JWTError si es inválido/expirado.
    """
    settings = get_settings()
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
