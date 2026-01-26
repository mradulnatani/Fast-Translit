from db import Base, engine
from models import UserSubmission

Base.metadata.create_all(bind=engine)

