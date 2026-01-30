from sqlalchemy import Column, Integer, String, DateTime
from .db import Base
from datetime import datetime

class UserSubmission(Base):
    __tablename__ = "user_submissions"

    id = Column(Integer, primary_key=True, index=True)
    pin_code = Column(Integer,nullable=False)
    state = Column(String,nullable=False)
    city = Column(String,nullable=False)
    locality = Column(String,nullable=False)
    landmark = Column(String,nullable=False)


class Normalized_data(Base):
    __tablename__ = "normalized_data"
    id = Column(Integer, primary_key=True)
    city_normalized = Column(String,nullable=False)
    state_normalzed = Column(String,nullable=False)
    locality_normalized = Column(String,nullable=False)
    landmark_normalized = Column(String,nullable=False)
