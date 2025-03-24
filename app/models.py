import uuid
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()


class AuthProviderEnum(PyEnum):
    EMAIL = "email"
    GOOGLE = "google"
    APPLE = "apple"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)

    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)
    confirmation_token = Column(String, unique=True, nullable=True)

    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    auth_provider = Column(Enum(AuthProviderEnum), default=AuthProviderEnum.EMAIL)
    third_party_id = Column(String, unique=True, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)