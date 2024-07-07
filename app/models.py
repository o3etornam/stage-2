from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Users(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String)


class Organisations(Base):
    __tablename__ = "organisations"

    orgId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True)


class Members(Base):
    __tablename__ = "members"

    orgId = Column(
        Integer,
        ForeignKey("organisations.orgId", ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )
    userId = Column(
        Integer,
        ForeignKey("users.userId", ondelete="cascade"),
        primary_key=True,
        nullable=False,
    )

    organisation = relationship("Organisations")
