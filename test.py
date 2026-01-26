from Backend.db import Base, engine
from Backend.models import Company,JWTToken,TargetApi, RequestLog
Base.metadata.create_all(bind=engine)

