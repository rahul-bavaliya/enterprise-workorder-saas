from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class LineOfBusinessBase(BaseModel):
    division_name: str = Field(
        ...,
        max_length=255,
        examples=["Construction & Forestry", "Agriculture", "Truck & Trailer"],
    )
    division_abbreviation: str | None = Field(
        None, max_length=50, examples=["C&F", "AG", "TT"]
    )
    lob_name: str = Field(
        ..., max_length=255, examples=["Construction", "Agriculture", "Trucking"]
    )
    is_active: bool = True


class LineOfBusinessCreate(LineOfBusinessBase):
    pass


class LineOfBusinessUpdate(BaseModel):
    division_name: str | None = Field(
        None,
        max_length=255,
        examples=["Construction & Forestry", "Agriculture", "Truck & Trailer"],
    )
    division_abbreviation: str | None = Field(
        None, max_length=50, examples=["C&F", "AG", "TT"]
    )
    lob_name: str | None = Field(
        None, max_length=255, examples=["Construction", "Agriculture", "Trucking"]
    )
    is_active: bool | None = None


class LineOfBusinessResponse(LineOfBusinessBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
