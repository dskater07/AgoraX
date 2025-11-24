"""
backend/app/schemas/user_schema.py

Esquemas Pydantic relacionados con usuarios del sistema AgoraX.

Se utilizan principalmente en:
- Autenticación (login, tokens JWT).
- Administración de usuarios (creación, lectura).
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Esquema base de usuario.

    Incluye los campos comunes que se exponen en las respuestas:
    - email: correo electrónico del usuario.
    - full_name: nombre completo.
    - role: rol del usuario (ADMIN u OWNER).
    """

    email: EmailStr
    full_name: Optional[str] = None
    role: str = "OWNER"


class UserCreate(UserBase):
    """
    Esquema de entrada para creación de usuario.

    Incluye el campo de contraseña en texto plano, que luego será hasheado
    en el modelo de dominio antes de persistirlo.
    """

    password: str


class UserRead(UserBase):
    """
    Esquema de salida para lectura de usuario.

    Incluye el identificador interno.
    """

    id: int

    class Config:
        """
        Permite crear instancias de este esquema directamente desde
        objetos ORM de SQLAlchemy (mode from_orm en Pydantic v1 / from_attributes en v2).
        """
        from_attributes = True


class Token(BaseModel):
    """
    Esquema de respuesta del token JWT.

    Utilizado en el endpoint de login.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Información mínima extraída de un JWT válido.

    Se utiliza internamente para obtener el usuario actual.
    """

    email: Optional[EmailStr] = None
