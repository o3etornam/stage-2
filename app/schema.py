from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: str

class User(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: EmailStr
    phone: str

class UserPublic(BaseModel):
    status: str = 'success'
    message: str = 'Registration Successful'
    data: "Token"
    user: User

class Organization(BaseModel):
    orgId: str
    name: str
    description: str

class Token(BaseModel):
    accessToken: str
