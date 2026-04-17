from enum import unique

from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=True, unique=True)
    user_email = Column(String, ForeignKey("users.email"))
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)