""""
from sqlalchemy import Column, Integer, String, DateTime
from Backend.db import Base
from datetime import datetime

class UserSubmission(Base):
    __tablename__ = "user_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
"""""

from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey,JSON,Text)
from sqlalchemy.orm import relationship
from datetime import datetime
from Backend.db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    hashed_secret = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    api_endpoints = relationship( "APIEndpoint",back_populates="company",cascade="all, delete-orphan")

    jwt_tokens = relationship("JWTToken",back_populates="company",cascade="all, delete-orphan")

    request_logs = relationship("RequestLog",back_populates="company",cascade="all, delete-orphan")



class APIEndpoint(Base):
    __tablename__ = "api_endpoints"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer,ForeignKey("companies.id", ondelete="CASCADE"),nullable=False)

    endpoint_key = Column(Text, nullable=False)
    target_url = Column(Text, nullable=False)

    fields_to_transliterate = Column(JSON, nullable=False)
    normalization_enabled = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="api_endpoints")

    request_logs = relationship("RequestLog",back_populates="api_endpoint",cascade="all, delete-orphan")



class JWTToken(Base):
    __tablename__ = "jwt_tokens"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer,ForeignKey("companies.id", ondelete="CASCADE"),nullable=False)

    jti = Column(Text, nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="jwt_tokens")

