# app/api/v1/schemas/customer.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class CustomerBase(BaseModel):
    name: str = Field(
        ..., max_length=255, description="The name of the customer", example="John Doe"
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=255,
        description="The email address of the customer",
        example="john.doe@example.com",
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="The phone number of the customer",
        example="123-456-7890",
    )
    address: Optional[str] = Field(
        None,
        max_length=500,
        description="The address of the customer",
        example="123 Main St, Anytown, USA",
    )


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(
        None, max_length=255, description="The name of the customer", example="John Doe"
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=255,
        description="The email address of the customer",
        example="john.doe@example.com",
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="The phone number of the customer",
        example="123-456-7890",
    )
    address: Optional[str] = Field(
        None,
        max_length=500,
        description="The address of the customer",
        example="123 Main St, Anytown, USA",
    )


class CustomerResponse(CustomerBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
