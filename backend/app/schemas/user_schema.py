from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class RoleEnum(str, Enum):
    admin = "admin"
    propietario = "propietario"
    revisor = "revisor"

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: RoleEnum = RoleEnum.propietario
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=64)

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=4, max_length=64)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True  # Permite construir desde ORM (SQLAlchemy)
    }
