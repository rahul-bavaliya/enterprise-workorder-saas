# app/modules/Make_product_model/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MakeProductModelResponse(BaseModel):
    id: str
    product_id: str
    model_id: Optional[int] = None
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    make: str
    model: str
    decal_model: Optional[str] = None
    category: str
    sub_category: Optional[str] = None
    division: Optional[str] = None
    jd_product_family: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MakeProductModelUploadSummary(BaseModel):
    total_processed: int
    inserted: int
    updated: int
    message: str