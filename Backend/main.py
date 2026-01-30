from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from Backend.db import SessionLocal
from Backend.schemas import UserForm, SubmissionResponse
from Backend.crud_helper import create_submission

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit", response_model=SubmissionResponse)
def submit_form(form: UserForm, db: Session = Depends(get_db)):
    submission = create_submission(db,form.pin_code, form.state, form.city, form.locality, form.landmark)

    return SubmissionResponse(
        id=submission.id,
        state_trans=submission.state,
        city_trans=submission.city,
        landmark_trans=submission.landmark,
        locality_trans=submission.locality
    )
