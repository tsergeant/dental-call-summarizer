from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)  # SERIAL by default
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    notes = Column(String, nullable=True)
