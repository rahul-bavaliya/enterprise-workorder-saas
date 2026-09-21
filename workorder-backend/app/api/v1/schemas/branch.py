# app/api/v1/schemas/branch.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class BranchBase(BaseModel):
    name: str = Field(..., max_length=255)
    number: Optional[int] = None
    lob_id: UUID
    business_id: UUID
    branch_manager_id: Optional[UUID] = None
    address1: Optional[str] = Field(None, max_length=500)
    address2: Optional[str] = Field(None, max_length=500)
    city: str = Field(..., max_length=255)
    postal_code: str = Field(..., max_length=20)
    province: str = Field(..., max_length=255)
    country: str = Field(..., max_length=255)
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)
    region: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=15)
    email: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=500)
    contact_person: Optional[str] = Field(None, max_length=255)
    division_name: str = Field(..., max_length=255)
    is_active: bool = True


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    number: Optional[int] = None
    lob_id: Optional[UUID] = None
    business_id: Optional[UUID] = None
    branch_manager_id: Optional[UUID] = None
    address1: Optional[str] = Field(None, max_length=500)
    address2: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=255)
    postal_code: Optional[str] = Field(None, max_length=20)
    province: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)
    region: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=15)
    email: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=500)
    contact_person: Optional[str] = Field(None, max_length=255)
    division_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class BranchResponse(BranchBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# LineOfBusiness schemas
class LineOfBusinessBase(BaseModel):
    lob_name: str = Field(..., max_length=255)
    is_active: bool = True


class LineOfBusinessCreate(LineOfBusinessBase):
    pass


class LineOfBusinessUpdate(BaseModel):
    lob_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class LineOfBusinessResponse(LineOfBusinessBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True