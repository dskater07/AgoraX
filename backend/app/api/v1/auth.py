"""
backend/app/api/v1/auth.py

Endpoints de autenticación y gestión básica de usuarios para AgoraX.

Incluye:
- /auth/login: Autenticación con email y contraseña, emisión de JWT.
- /auth/me: Consulta del usuario actual autenticado.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
)
from app.models import User
from app.schemas.user_schema import UserCreate, UserRead, Token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.

    NOTA ACADÉMICA:
        - En un entorno productivo, probablemente no se expondría un endpoint
          de registro general, sino que estaría restringido a administradores.

    Regla de negocio relacionada:
        - RD-03: Solo usuarios autenticados pueden votar (este endpoint permite
          crear dichas identidades).
    """
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese email.",
        )

    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Autentica a un usuario existente y devuelve un token JWT.

    Implementa:
        - Verificación de credenciales (email + password).
        - Generación de token JWT con create_access_token.

    Regla:
        - RD-03: Solo usuarios autenticados pueden votar (a partir de este token).
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    access_token = create_access_token(subject=user.email)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Devuelve la información del usuario autenticado actual.

    Se basa en el token JWT enviado en la cabecera Authorization.
    """
    return current_user
