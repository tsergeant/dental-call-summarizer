from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import SessionLocal
from app.models import Call, Customer
from app.schemas.commlog import CommLogResponse, CommLogEntry, CustomerOption
from app.schemas.call import CallCreate, CallOut
from app.ai.openai_client import summarize_transcript, generate_dummy_transcript
from datetime import datetime
import random

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
    return {"message": f"Hello from {call.phone_number}"}

@router.get("/api/commlog", response_model=CommLogResponse)
def get_commlog(db: Session = Depends(get_db)):
    calls = (
        db.query(Call)
        .options(joinedload(Call.customer))
        .order_by(Call.timestamp.desc())
        .all()
    )

    call_entries = [
        CommLogEntry(
            call_id=call.call_id,
            timestamp=call.timestamp,
            phone_number=call.phone_number,
            summary_text=call.summary_text,
            customer_id=call.customer_id,
            customer_name=call.customer.name if call.customer else None
        )
        for call in calls
    ]

    customers = db.query(Customer).order_by(Customer.name).all()
    customer_options = [CustomerOption(customer_id=c.customer_id, name=c.name) for c in customers]

    return CommLogResponse(calls=call_entries, customers=customer_options)

@router.get("/api/calls/generate-transcript")
def generate_transcript():
    participants = [
        "Susan (Receptionist)",
        "Alex (Receptionist)",
        "Karen (Billing)",
        "Max (Dental Hygienist)",
        "Mary (Dentist)"
    ]
    phone_number = f"5550000{random.randint(1, 99):03d}"
    direction = random.choice(["Incoming", "Outgoing"])
    office_participant = random.sample(participants, random.randint(1, 2))
    office_list = "; ".join(office_participant)

    transcript = generate_dummy_transcript(direction, phone_number, office_list)
    return {"transcript": transcript}

@router.post("/api/calls/", response_model=CallOut)
def create_call(call_data: CallCreate, db: Session = Depends(get_db)):
    try:
        summary = summarize_transcript(call_data.transcription_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    call = Call(
        phone_number=call_data.phone_number,
        timestamp=call_data.timestamp or datetime.utcnow(),
        transcription_text=call_data.transcription_text,
        summary_text=summary,
        direction=call_data.direction,
        office_person=call_data.office_person,
    )
    db.add(call)
    db.commit()
    db.refresh(call)
    return call
