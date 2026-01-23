from Backend.db import Base, engine
#from Backend.models import Client, Token, TransliterationRequest
from Backend.models import RequestLog, JWTToken, APIEndpoint, Company
Base.metadata.create_all(bind=engine)

