from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CommLogEntry(BaseModel):
    call_id: int
    timestamp: datetime
    phone_number: str
    summary_text: str
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None

    class Config:
        orm_mode = True


class CustomerOption(BaseModel):
    customer_id: int
    name: str

    class Config:
        orm_mode = True


class CommLogResponse(BaseModel):
    calls: List[CommLogEntry]
    customers: List[CustomerOption]
