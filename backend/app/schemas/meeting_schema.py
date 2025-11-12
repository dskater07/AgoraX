from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class MeetingStatusEnum(str, Enum):
    pendiente = "pendiente"
    abierta = "abierta"
    cerrada = "cerrada"

class MeetingBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    start_time: datetime
    quorum_min: float = Field(51.0, ge=0, le=100)

class MeetingCreate(MeetingBase):
    pass

class MeetingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    start_time: Optional[datetime] = None
    quorum_min: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[MeetingStatusEnum] = None

class MeetingOut(MeetingBase):
    id: int
    status: MeetingStatusEnum
    created_at: datetime
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
