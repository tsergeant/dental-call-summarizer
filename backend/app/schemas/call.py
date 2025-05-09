from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class CallCreate(BaseModel):
    phone_number: str
    transcription_text: str
    timestamp: Optional[datetime] = None
    direction: Literal["incoming", "outgoing"]
    office_person: Optional[str]

class CallOut(BaseModel):
    call_id: int
    phone_number: str
    timestamp: datetime
    transcription_text: str
    summary_text: str
    direction: str
    office_person: Optional[str]

    class Config:
        orm_mode = True
