from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Call(Base):
    __tablename__ = "calls"
    customer = relationship("Customer", backref="calls", lazy="joined")
    call_id = Column(Integer, primary_key=True, index=True)  # SERIAL by default
    direction = Column(String, nullable=False)  # 'incoming' or 'outgoing'
    office_person = Column(String, nullable=True)  # e.g., 'Susan (Receptionist)'
    timestamp = Column(DateTime, default=datetime.utcnow)
    phone_number = Column(String, nullable=False)
    summary_text = Column(Text, nullable=False)
    transcription_text = Column(Text, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
