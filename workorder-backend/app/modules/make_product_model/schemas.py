# app/modules/Make_product_model/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from uuid import UUID


class MakeProductModelCreate(BaseModel):
    product_id: int = Field(
        ...,
        description="Unique identifier for the product",
        examples=[12345],
    )
    model_id: Optional[int] = Field(
        None, description="Identifier for the model", examples=[101]
    )
    category_id: Optional[int] = Field(
        None, description="Identifier for the category", examples=[10]
    )
    sub_category_id: Optional[int] = Field(
        None, description="Identifier for the sub-category", examples=[5]
    )
    make: str = Field(
        ..., max_length=255, description="Make of the product", examples=["John Deere"]
    )
    model: str = Field(
        ..., max_length=500, description="Model of the product", examples=["X1"]
    )
    decal_model: Optional[str] = Field(
        None, max_length=500, description="Decal model of the product", examples=["D1"]
    )
    category: str = Field(
        ...,
        max_length=255,
        description="Category of the product",
        examples=["Tractors"],
    )
    sub_category: Optional[str] = Field(
        None,
        max_length=255,
        description="Sub-category of the product",
        examples=["Utility Tractors"],
    )
    division: Optional[str] = Field(
        None,
        max_length=100,
        description="Division of the product",
        examples=["Agricultural"],
    )
    jd_product_family: Optional[str] = Field(
        None,
        max_length=255,
        description="John Deere product family",
        examples=["Family A"],
    )


class MakeProductModelResponse(BaseModel):
    id: UUID = Field(
        ..., description="Unique identifier for the MakeProductModel", examples=["1"]
    )
    product_id: int = Field(
        ...,
        description="Unique identifier for the product",
        examples=[12345],
    )
    model_id: Optional[int] = Field(
        None, description="Identifier for the model", examples=[101]
    )
    category_id: Optional[int] = Field(
        None, description="Identifier for the category", examples=[10]
    )
    sub_category_id: Optional[int] = Field(
        None, description="Identifier for the sub-category", examples=[5]
    )
    make: str = Field(
        ..., max_length=255, description="Make of the product", examples=["John Deere"]
    )
    model: str = Field(
        ..., max_length=500, description="Model of the product", examples=["X1"]
    )
    decal_model: Optional[str] = Field(
        None, max_length=500, description="Decal model of the product", examples=["D1"]
    )
    category: str = Field(
        ...,
        max_length=255,
        description="Category of the product",
        examples=["Tractors"],
    )
    sub_category: Optional[str] = Field(
        None,
        max_length=255,
        description="Sub-category of the product",
        examples=["Utility Tractors"],
    )
    division: Optional[str] = Field(
        None,
        max_length=100,
        description="Division of the product",
        examples=["Agricultural"],
    )
    jd_product_family: Optional[str] = Field(
        None,
        max_length=255,
        description="John Deere product family",
        examples=["Family A"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the record was created",
        examples=["2024-01-01T12:00:00Z"],
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the record was last updated",
        examples=["2024-01-02T12:00:00Z"],
    )

    class Config:
        from_attributes = True


class MakeProductModelUploadSummary(BaseModel):
    total_processed: int
    inserted: int
    updated: int
    message: str


class MakeProductModelUpdate(BaseModel):
    product_id: Optional[int] = Field(
        None,
        description="Unique identifier for the product",
        examples=[12345],
    )
    model_id: Optional[int] = Field(
        None, description="Identifier for the model", examples=[101]
    )
    category_id: Optional[int] = Field(
        None, description="Identifier for the category", examples=[10]
    )
    sub_category_id: Optional[int] = Field(
        None, description="Identifier for the sub-category", examples=[5]
    )
    make: Optional[str] = Field(
        None, max_length=255, description="Make of the product", examples=["John Deere"]
    )
    model: Optional[str] = Field(
        None, max_length=500, description="Model of the product", examples=["X1"]
    )
    decal_model: Optional[str] = Field(
        None, max_length=500, description="Decal model of the product", examples=["D1"]
    )
    category: Optional[str] = Field(
        None,
        max_length=255,
        description="Category of the product",
        examples=["Tractors"],
    )
    sub_category: Optional[str] = Field(
        None,
        max_length=255,
        description="Sub-category of the product",
        examples=["Utility Tractors"],
    )
    division: Optional[str] = Field(
        None,
        max_length=100,
        description="Division of the product",
        examples=["Agricultural"],
    )
    jd_product_family: Optional[str] = Field(
        None,
        max_length=255,
        description="John Deere product family",
        examples=["Family A"],
    )
