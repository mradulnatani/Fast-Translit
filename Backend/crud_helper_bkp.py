from sqlalchemy.orm import Session
from .models import UserSubmission
from .translit import transliterate_text

def create_submission(db: Session, pin_code:int,state: str, city: str,locality: str,landmark: str):
    state_trans = transliterate_text(state)
    city_trans = transliterate_text(city)
    locality_trans = transliterate_text(locality)
    landmark_trans = transliterate_text(landmark)

    submission = UserSubmission(
        state=state_trans,
        city=city_trans,
        locality=locality_trans,
        landmark=landmark_trans,
        pin_code = pin_code
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission

