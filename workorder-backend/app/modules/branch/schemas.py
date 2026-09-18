from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, HttpUrl, StringConstraints
from typing import Annotated

# Pure Pydantic regex type validation for clean 10-15 digit phone formats (e.g., +1234567890)
PhoneStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=10,
        max_length=15,
        pattern=r"^\+?[1-9]\d{9,14}$",
    ),
]


class BranchBase(BaseModel):
    # Branch Details
    name: str = Field(
        ...,
        max_length=255,
        description="The name of the branch",
        examples=["Main Branch", "Downtown Branch", "Uptown Branch"],
    )

    is_active: bool = Field(
        default=True,
        description="Indicates if the branch is active",
        examples=[True, False],
    )

    # Branch Location Details
    address1: str | None = Field(
        default=None, max_length=500, examples=["123 Main St", "456 Oak Ave"]
    )
    address2: str | None = Field(
        default=None, max_length=500, examples=["Apt 101", "Suite 200"]
    )
    city: str = Field(
        ..., max_length=255, examples=["New York", "Los Angeles", "Chicago"]
    )
    postal_code: str = Field(
        ..., max_length=20, examples=["S4N 0T9", "S4N 0T1", "60601"]
    )
    province: str = Field(..., max_length=255, examples=["SK", "AB", "BC"])
    country: str = Field(..., max_length=255, examples=["USA", "Canada", "Mexico"])
    region: str | None = Field(
        default=None, max_length=255, examples=["North", "South", "East", "West"]
    )
    latitude: Decimal | None = Field(
        default=None,
        ge=-90,
        le=90,
        description="GPS Latitude",
        examples=[Decimal("40.7128"), Decimal("-33.8688")],
    )
    longitude: Decimal | None = Field(
        default=None,
        ge=-180,
        le=180,
        description="GPS Longitude",
        examples=[Decimal("-74.0060"), Decimal("151.2093")],
    )

    # Branch Contact Details
    phone: PhoneStr | None = Field(
        default=None,
        description="Valid telephone string between 10-15 digits",
        examples=["+1234567890", "+1987654321"],
    )
    email: EmailStr | None = Field(
        default=None,
        description="Contact email address",
        examples=["contact@branch.com"],
    )
    website_url: HttpUrl | str | None = Field(
        default=None,
        max_length=500,
        description="Website URL of the branch",
        examples=["https://maps.app.goo.gl/xAJZB7B4KBu3yw5f7"],
    )
    contact_person: str | None = Field(
        default=None,
        max_length=255,
        description="Name of the contact person for the branch",
        examples=["John Doe", "Jane Smith"],
    )
    lob_id: UUID = Field(
        ...,
        description="The UUID of the associated Line of Business",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    # Make all payload fields optional for partial PATCH updates
    name: str | None = Field(
        None,
        max_length=255,
        description="The name of the branch",
        examples=["Main Branch", "Downtown Branch", "Uptown Branch"],
    )
    division_name: str | None = Field(
        None,
        max_length=255,
        description="The name of the division",
        examples=["Sales", "Marketing", "IT"],
    )
    lob_name: str | None = Field(
        None,
        max_length=255,
        description="The name of the line of business",
        examples=["Retail", "Wholesale", "E-commerce"],
    )
    is_active: bool | None = None

    address1: str | None = Field(
        None,
        max_length=500,
        description="The first line of the branch address",
        examples=["123 Main St", "456 Oak Ave"],
    )
    address2: str | None = Field(
        None,
        max_length=500,
        description="The second line of the branch address",
        examples=["Apt 1", "Suite 2"],
    )
    city: str | None = Field(
        None,
        max_length=255,
        description="The city where the branch is located",
        examples=["New York", "Los Angeles"],
    )
    postal_code: str | None = Field(
        None,
        max_length=20,
        description="The postal code of the branch address",
        examples=["10001", "90210"],
    )
    province: str | None = Field(
        None,
        max_length=255,
        description="The province or state where the branch is located",
        examples=["NY", "CA"],
    )
    country: str | None = Field(
        None,
        max_length=255,
        description="The country where the branch is located",
        examples=["USA", "Canada"],
    )
    region: str | None = Field(
        None,
        max_length=255,
        description="The region where the branch is located",
        examples=["Northeast", "West"],
    )
    latitude: Decimal | None = Field(
        None,
        ge=-90,
        le=90,
        description="GPS Latitude",
        examples=[Decimal("40.7128"), Decimal("-33.8688")],
    )
    longitude: Decimal | None = Field(
        None,
        ge=-180,
        le=180,
        description="GPS Longitude",
        examples=[Decimal("-74.0060"), Decimal("-118.2437")],
    )

    phone: PhoneStr | None = Field(
        None,
        description="The phone number of the branch",
        examples=["+1234567890", "+1987654321"],
    )
    email: EmailStr | None = Field(
        None,
        description="The email address of the branch",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    website_url: HttpUrl | str | None = Field(
        None, max_length=500, description="The website URL of the branch"
    )
    contact_person: str | None = Field(
        None,
        max_length=255,
        description="The name of the contact person for the branch",
        examples=["John Doe", "Jane Smith"],
    )

    lob_id: UUID = Field(
        ...,
        description="The UUID of the associated Line of Business",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class BranchResponse(BranchBase):
    id: UUID
    # lob_id: UUID
    number: int = Field(
        ..., description="The database auto-incremented sequence number"
    )
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
