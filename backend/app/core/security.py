"""
backend/app/core/security.py

Funciones de seguridad del backend AgoraX.

Incluye:
- Gestión de contraseñas (hash y verificación).
- Manejo de JWT (creación y validación de tokens).
- Obtención del usuario actual (get_current_user).
- Cifrado y descifrado de votos (RD-06).
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
from app.models import User

settings = get_settings()

# ================== CONTRASEÑAS ==================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña en texto plano contra su hash.

    :param plain_password: Contraseña provista por el usuario.
    :param hashed_password: Hash almacenado en base de datos.
    :return: True si coincide, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera el hash seguro para una contraseña.

    :param password: Contraseña en texto plano.
    :return: Cadena hasheada lista para persistir.
    """
    return pwd_context.hash(password)


# ================== JWT ==================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    """
    Crea un token JWT para el usuario autenticado.

    :param subject: Identificador único (por ejemplo, email del usuario).
    :param expires_minutes: Minutos hasta la expiración del token.
    :return: Token JWT como cadena.
    """
    if expires_minutes is None:
        expires_minutes = settings.JWT_EXPIRE_MINUTES

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire}

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def _get_db_for_security():
    """
    Crea una sesión de base de datos exclusiva para funciones de seguridad.

    Esta función se usa internamente en get_current_user.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(_get_db_for_security),
) -> User:
    """
    Obtiene el usuario actual a partir del JWT enviado en la cabecera Authorization.

    Implementa RD-03: Solo usuarios autenticados pueden votar.

    :raises HTTPException: Si el token es inválido o el usuario no existe.
    :return: Instancia de User.
    """
    cred_exc = HTTPException(
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
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise cred_exc

    return user


# ================== CIFRADO DE VOTOS (RD-06) ==================

if settings.VOTE_ENCRYPTION_KEY:
    _key = settings.VOTE_ENCRYPTION_KEY.encode("utf-8")
else:
    # Clave generada dinámicamente para entornos de desarrollo
    _key = Fernet.generate_key()

_fernet = Fernet(_key)


def encrypt_vote_value(value: str) -> str:
    """
    Cifra el valor de un voto antes de almacenarlo (RD-06).

    :param value: Opción de voto en texto claro.
    :return: Cadena cifrada (base64).
    """
    token = _fernet.encrypt(value.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_vote_value(value_encrypted: str) -> str:
    """
    Descifra el valor cifrado de un voto, para uso en agregaciones o auditoría.

    :param value_encrypted: Valor cifrado almacenado.
    :return: Valor en texto claro.
    """
    return _fernet.decrypt(value_encrypted.encode("utf-8")).decode("utf-8")
