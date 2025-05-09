from fastapi import FastAPI
from . import models, database, routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or limit to ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

@app.on_event("startup")
def startup():
    db = database.SessionLocal()
    if not db.query(models.Call).first():
        db.add(models.Call(caller_info="Jane Doe"))
        db.commit()
    db.close()

app.include_router(routes.router)
