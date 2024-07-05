from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String, unique=True, index=True)
    lastName = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime)


class Organizzation(Base):
    __tablename__ = "organization"

    orgId = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    ownerId = Column(Integer, ForeignKey("users.userId"))