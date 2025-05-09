from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Define declarative base
class Base(DeclarativeBase):
    pass