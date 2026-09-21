# app/api/v1/schemas/asset.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class AssetCategory(str, Enum):
    HVAC = "hvac"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    MACHINERY = "machinery"
    IT_INFRASTRUCTURE = "it_infrastructure"


class AssetBase(BaseModel):
    customer_id: UUID
    name: str = Field(..., max_length=255)
    category: AssetCategory
    serial_number: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    category: Optional[AssetCategory] = None
    serial_number: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)


class AssetResponse(AssetBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True