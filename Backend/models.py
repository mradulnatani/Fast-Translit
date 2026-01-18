from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from Backend.db import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    target_api_url = Column(String, nullable=False)
    fields_to_transliterate = Column(String)  # comma-separated or JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    requests = relationship("TransliterationRequest", back_populates="client", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="client", cascade="all, delete-orphan")


class TransliterationRequest(Base):
    __tablename__ = "transliteration_requests"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))
    input_payload = Column(JSON, nullable=False)   # whatever the client sends
    output_payload = Column(JSON, nullable=False)  # transliterated result
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="requests")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    jti = Column(String, unique=True, index=True, nullable=False)  # JWT ID
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)

    client = relationship("Client", back_populates="tokens")

