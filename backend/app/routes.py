from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Call

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/hello")
def read_hello(db: Session = Depends(get_db)):
    call = db.query(Call).first()
    return {"message": f"Hello from {call.caller_info}"}
