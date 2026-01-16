from sqlalchemy.orm import Session
from models import UserSubmission
from translit import transliterate_text
import re

# Detect if text is in Devanagari (Hindi)
def is_hindi(text: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', text))

def create_submission(db: Session, name: str, address: str):
    
    name_trans = transliterate_text(name) if is_hindi(name) else name
    address_trans = transliterate_text(address) if is_hindi(address) else address

    submission = UserSubmission(
        name=name_trans,
        address=address_trans
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

