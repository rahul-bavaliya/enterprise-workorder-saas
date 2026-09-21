# app/api/v1/schemas/line_of_business.py
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class LineOfBusinessBase(BaseModel):
    division_name: str = Field(
        ...,
        max_length=255,
        description="The division name",
        examples=["Construction", "Manufacturing", "Retail"],
    )
    division_abbreviation: Optional[str] = Field(
        None,
        max_length=50,
        description="The division abbreviation",
        examples=["CON", "MFG", "RET"],
    )
    lob_name: str = Field(
        ...,
        max_length=255,
        description="The name of the line of business",
        examples=["Retail", "Wholesale", "E-commerce"],
    )
    is_active: bool = Field(
        default=True,
        description="Indicates if the line of business is active",
        examples=[True, False],
    )


class LineOfBusinessCreate(LineOfBusinessBase):
    pass


class LineOfBusinessUpdate(BaseModel):
    division_name: Optional[str] = Field(None, max_length=255)
    division_abbreviation: Optional[str] = Field(None, max_length=50)
    lob_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class LineOfBusinessResponse(LineOfBusinessBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True