from sqlalchemy import Column, Integer, String
from .database import Base

class Call(Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True, index=True)
    caller_info = Column(String, nullable=False)
