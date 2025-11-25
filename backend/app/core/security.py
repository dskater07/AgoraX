"""
backend/app/core/security.py

Funciones y utilidades de seguridad para AgoraX:

- Hash y verificación de contraseñas.
- Creación y validación de tokens JWT.
- Dependencia get_current_user para obtener el usuario autenticado.

Se integra con:
    - app.core.config.Settings (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
    - app.core.db.get_db
    - app.schemas.TokenData
"""

from datetime import datetime, timedelta
from typing import Optional, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.schemas import TokenData

# Contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para extraer el token de la cabecera Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# =========================================================
# Gestión de contraseñas
# =========================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña en texto plano coincida con el hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro de la contraseña.
    """
    return pwd_context.hash(password)


# =========================================================
# Gestión de JWT
# =========================================================

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Crea un token JWT de acceso.

    Parámetros:
        subject: Identificador del sujeto (normalmente email del usuario).
        expires_delta: Tiempo de expiración; si no se envía, se usa
                       ACCESS_TOKEN_EXPIRE_MINUTES de la configuración.

    Devuelve:
        Token JWT como cadena.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


# =========================================================
# Usuario actual a partir del token
# =========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Any:
    """
    Obtiene el usuario actual autenticado a partir del token JWT.

    Pasos:
        1. Decodifica el token usando SECRET_KEY y ALGORITHM.
        2. Extrae el campo "sub" (email del usuario).
        3. Consulta en la base de datos el usuario con ese email.
        4. Si algo falla, lanza HTTP 401.

    Devuelve:
        Instancia de User correspondiente al token.
    """
    # Importación diferida para evitar ciclos de importación
    from app.models.user import User

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        sub: Optional[str] = payload.get("sub")
        if sub is None:
            raise credentials_exception

        token_data = TokenData(username=sub)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user
