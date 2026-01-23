from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from Backend.db import SessionLocal
from Backend.schemas import UserForm, SubmissionResponse
from Backend.crud_helper import create_submission
from Backend.rabbitmq import send_notification

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit", response_model=SubmissionResponse)
def submit_form(form: UserForm, db: Session = Depends(get_db)):
    submission = create_submission(db, form.name, form.address)

    send_notification(
        f"New submission: {submission.name}, {submission.address}"
    )

    return SubmissionResponse(
        id=submission.id,
        name_trans=submission.name,
        address_trans=submission.address
    )


