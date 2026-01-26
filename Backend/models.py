from sqlalchemy import Column, Integer, JSON, Text, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    target_apis = relationship("TargetApi",back_populates="company",cascade="all, delete-orphan")

    jwt_tokens = relationship("JWTToken",back_populates="company",cascade="all, delete-orphan")

    request_logs = relationship("RequestLog",back_populates="company",cascade="all, delete-orphan")


class JWTToken(Base):
    __tablename__ = "jwt_token"

    id = Column(Integer, primary_key=True)
    jti = Column(String, nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    company = relationship("Company", back_populates="jwt_tokens")


class TargetApi(Base):
    __tablename__ = "target_api"

    id = Column(Integer, primary_key=True)
    endpoint_key = Column(String, nullable=False)
    target_api_url = Column(String, nullable=False)
    transliteration_fields = Column(JSON, nullable=False)

    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    company = relationship("Company", back_populates="target_apis")

    request_logs = relationship("RequestLog",back_populates="api_endpoint",cascade="all, delete-orphan")


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer,ForeignKey("company.id", ondelete="CASCADE"),nullable=False)

    api_endpoint_id = Column(Integer,ForeignKey("target_api.id", ondelete="CASCADE"),nullable=False)

    input_payload = Column(JSON, nullable=False)
    output_payload = Column(JSON, nullable=False)
    status_code = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="request_logs")
    api_endpoint = relationship("TargetApi", back_populates="request_logs")

