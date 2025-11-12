from pydantic import BaseModel, Field
from datetime import datetime

class AuditCreate(BaseModel):
    event_type: str = Field(..., max_length=50)
    user_email: str | None = None
    description: str | None = None

class AuditOut(AuditCreate):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
