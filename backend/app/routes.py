from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Call
from datetime import datetime
from app.constants import DUMMY_TRANSCRIPT
import random
import os

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

@router.get("/api/calls/generate-transcript")
def generate_dummy_transcript():
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

    system_prompt = """You are simulating a realistic phone call transcript for a dental office. The format should follow this exact structure:

Metadata: <timestamp>; <Incoming or Outgoing>; <caller phone number>; <office participants>
Office: <line of dialog>
Caller: <line of dialog>
... (repeated as needed)

Rules:
- Only include two roles: Office and Caller
- Use natural, realistic dialogue based on typical dental office calls
- Metadata must include actual participant names and roles (e.g., "Susan (Receptionist)")
- If the call is transferred, list all office participants in the metadata
- Keep it under 12 turns total
- Match tone and structure to the example below

Example:
Metadata: 2025-05-08 09:14; Incoming; 5550000001; Susan (Receptionist)
Office: Hello, this is ACME Dental. This is Susan at the front desk—how can I help you?
Caller: Hi, I was in for a filling last week and I'm still having some pain...
"""

    user_prompt = f"Generate a transcript with metadata: {direction}; {phone_number}; {office_list}"

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    return {"transcript": response.choices[0].message.content.strip()}


from fastapi import HTTPException
from app.ai.openai_client import summarize_transcript
from app.schemas.call import CallCreate, CallOut  # You'll create these below
from app.models.call import Call

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
