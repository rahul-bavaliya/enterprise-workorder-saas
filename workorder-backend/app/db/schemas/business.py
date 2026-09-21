# app/api/v1/schemas/business.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class BusinessBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    email: Optional[EmailStr] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    address1: Optional[str] = Field(None, max_length=500)
    address2: Optional[str] = Field(None, max_length=500)
    city: str = Field(..., max_length=255)
    state: Optional[str] = Field(None, max_length=100)
    country: str = Field(..., max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    website_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    email: Optional[EmailStr] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    address1: Optional[str] = Field(None, max_length=500)
    address2: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=255)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    website_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class BusinessResponse(BusinessBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True