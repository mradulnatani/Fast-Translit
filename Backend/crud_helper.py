from sqlalchemy.orm import Session
from .models import UserSubmission
from .translit import transliterate_text

def create_submission(db: Session, name: str, address: str):
    name_trans = transliterate_text(name)
    address_trans = transliterate_text(address)

    submission = UserSubmission(
        name=name_trans,
        address=address_trans
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission

