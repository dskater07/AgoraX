from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class VoteOptionEnum(str, Enum):
    si = "Sí"
    no = "No"
    abstencion = "Abstención"

class VoteCreate(BaseModel):
    meeting_id: int
    vote_option: VoteOptionEnum = Field(..., description="Opciones: Sí / No / Abstención")

class VoteOut(BaseModel):
    id: int | None = None
    meeting_id: int
    user_id: int | None = None
    user_email: str | None = None
    vote_option: VoteOptionEnum
    ip_address: str | None = None
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
