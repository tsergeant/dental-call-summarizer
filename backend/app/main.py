import os
import random
from datetime import datetime, timedelta

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.db.session import engine, SessionLocal
from app.models import Call
from app.models import Customer
from app.db import Base
from app.constants import DUMMY_TRANSCRIPT


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_triggers():
    with engine.connect() as conn:
        with open("app/db/triggers.sql", "r") as f:
            sql = f.read()
            try:
                conn.exec_driver_sql(sql)
                conn.commit()
            except Exception as e:
                if "already exists" in str(e).lower():
                    print("Trigger(s) already exist — skipping.")
                else:
                    raise e



@app.on_event("startup")
def show_routes():
    print("Registered routes:")
    for route in app.routes:
        print(f"{route.path} → {route.methods}")

def startup():
    if os.getenv("RESET_DB", "false").lower() == "true":
        Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    run_triggers()

    db: Session = SessionLocal()

    # Seed customer data
    customers = [
        Customer(name="Jane Doe", phone_number="5550000001"),
        Customer(name="John Smith", phone_number="5550000002"),
        Customer(name="Alice Johnson", phone_number="5550000003"),
        Customer(name="Bob Lee", phone_number="5550000004"),
        Customer(name="Cathy Brown", phone_number="5550000005"),
        Customer(name="David Wilson", phone_number="5550000006"),
        Customer(name="Ella Martinez", phone_number="5550000007"),
        Customer(name="Frank Harris", phone_number="5550000008"),
        Customer(name="Grace Hall", phone_number="5550000009"),
        Customer(name="Henry Young", phone_number="5550000010"),
    ]
    db.add_all(customers)
    db.commit()

    multi_call_customers = customers[:5]
    one_call_customers = customers[5:8]

    

    def generate_call(phone, days_ago, text):
        return Call(
            phone_number=phone,
            timestamp=datetime.utcnow() - timedelta(days=days_ago),
            summary_text=f"Summary for {text}",
            transcription_text=DUMMY_TRANSCRIPT,
        )

    calls = []

    for cust in multi_call_customers:
        for i in range(random.randint(2, 4)):
            calls.append(generate_call(
                cust.phone_number,
                days_ago=random.randint(0, 30),
                text=f"{cust.name} call {i+1}"
            ))

    for cust in one_call_customers:
        calls.append(generate_call(
            cust.phone_number,
            days_ago=random.randint(0, 30),
            text=f"{cust.name} call"
        ))

    for i in range(10):
        phone = f"55599999{i:02d}"
        calls.append(generate_call(
            phone,
            days_ago=random.randint(0, 30),
            text=f"Unlinked call {i+1}"
        ))

    db.add_all(calls)
    db.commit()
    db.close()

# Load API routes
from app import routes
app.include_router(routes.router)
