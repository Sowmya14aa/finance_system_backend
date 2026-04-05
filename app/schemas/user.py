from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.VIEWER

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models