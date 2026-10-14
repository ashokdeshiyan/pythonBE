
# models.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "Chatusers"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    phone = Column(String(15), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True, index=True)

    password_hash = Column(String(255), nullable=False)

    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    role = Column(String(20), nullable=False, server_default="user")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
