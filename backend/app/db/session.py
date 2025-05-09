from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base  # Import the base class from base.py

SQLALCHEMY_DATABASE_URL = "postgresql://calls:callsdbpass@db:5432/callsdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
