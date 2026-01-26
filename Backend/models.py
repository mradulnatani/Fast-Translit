from sqlalchemy import Column, Integer, String, DateTime
from .db import Base
from datetime import datetime

class UserSubmission(Base):
    __tablename__ = "user_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
