from Backend.db import Base, engine
# from Backend.models import Client, Token, TransliterationRequest
from Backend.models import UserSubmission
Base.metadata.create_all(bind=engine)

