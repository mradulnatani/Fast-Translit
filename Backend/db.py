from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_url = os.getenv("DATABASE_URL")

engine = create_engine(DB_url, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

