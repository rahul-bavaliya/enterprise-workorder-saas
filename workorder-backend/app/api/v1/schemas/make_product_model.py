# app/api/v1/schemas/make_product_model.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class MakeProductModelBase(BaseModel):
    product_id: int
    model_id: Optional[int] = None
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    make: str = Field(..., max_length=255)
    model: str = Field(..., max_length=500)
    decal_model: Optional[str] = Field(None, max_length=500)
    category: str = Field(..., max_length=255)
    sub_category: Optional[str] = Field(None, max_length=255)
    division: Optional[str] = Field(None, max_length=100)
    jd_product_family: Optional[str] = Field(None, max_length=255)


class MakeProductModelCreate(MakeProductModelBase):
    pass


class MakeProductModelUpdate(BaseModel):
    product_id: Optional[int] = None
    model_id: Optional[int] = None
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    make: Optional[str] = Field(None, max_length=255)
    model: Optional[str] = Field(None, max_length=500)
    decal_model: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=255)
    sub_category: Optional[str] = Field(None, max_length=255)
    division: Optional[str] = Field(None, max_length=100)
    jd_product_family: Optional[str] = Field(None, max_length=255)


class MakeProductModelResponse(MakeProductModelBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True