from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True, index=True)
    fullName = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    passwordHash = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)