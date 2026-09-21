# app/api/v1/schemas/user.py
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.db.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        max_length=255,
        description="The email address of the user",
        example="john.doe@example.com",
    )
    role: UserRole = Field(
        default=UserRole.TECHNICIAN,
        description="The role of the user",
        example=UserRole.TECHNICIAN,
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        description="The password of the user",
        example="password@123",
    )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(
        None,
        max_length=255,
        description="The email address of the user",
        example="john.doe@example.com",
    )
    role: Optional[UserRole] = Field(
        None, description="The role of the user", example=UserRole.TECHNICIAN
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=255,
        description="The password of the user",
        example="securepassword",
    )


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserDeleteResponse(BaseModel):
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
    )
