# app/api/v1/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.db.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    role: UserRole = Field(default=UserRole.TECHNICIAN)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=8, max_length=255)


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True