from Backend.db import Base, engine
from Backend.models import Company,JWTToken,TargetApi
Base.metadata.create_all(bind=engine)

