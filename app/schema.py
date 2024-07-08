from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: Optional[str] = Field(None, pattern=r"^\+?\d{9,15}$")


class User(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: EmailStr
    phone: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Data(BaseModel):
    accessToken: str
    user: User


class UserPublic(BaseModel):
    status: str = "success"
    message: str
    data: Data


class AddUser(BaseModel):
    userId: int


class OrganisationCreate(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class Organisation(BaseModel):
    orgId: str
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class OrganisationPublic(BaseModel):
    status: str = "success"
    message: str = "<message>"
    data: Organisation


class Token(BaseModel):
    accessToken: str


class TokenData(BaseModel):
    access_token: str
    token_type: str = "Bearer"
