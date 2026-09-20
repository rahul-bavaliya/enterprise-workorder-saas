# app/api/v1/schemas/work_order.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.db.models.work_order import AssetCategory, WorkOrderPriority


class AssetBase(BaseModel):
    name: str = Field(..., max_length=255)
    category: AssetCategory
    serial_number: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)


class AssetCreate(AssetBase):
    customer_id: UUID


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    category: Optional[AssetCategory] = None
    serial_number: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)


class AssetResponse(AssetBase):
    id: UUID
    customer_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class WorkOrderBase(BaseModel):
    customer_id: UUID
    asset_id: UUID
    status_id: UUID
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
    sales_type_id: UUID
    assigned_technician_id: Optional[UUID] = None


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrderUpdate(BaseModel):
    customer_id: Optional[UUID] = None
    asset_id: Optional[UUID] = None
    status_id: Optional[UUID] = None
    priority: Optional[WorkOrderPriority] = None
    sales_type_id: Optional[UUID] = None
    assigned_technician_id: Optional[UUID] = None


class WorkOrderResponse(WorkOrderBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkOrderTaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    is_completed: bool = False


class WorkOrderTaskCreate(WorkOrderTaskBase):
    work_order_id: UUID


class WorkOrderTaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    is_completed: Optional[bool] = None


class WorkOrderTaskResponse(WorkOrderTaskBase):
    id: UUID
    work_order_id: UUID

    class Config:
        from_attributes = True


# Lookup schemas
class WorkOrderStatusLookupBase(BaseModel):
    name: str = Field(..., max_length=50)
    abbreviation: str = Field(..., max_length=10)
    description: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class WorkOrderStatusLookupCreate(WorkOrderStatusLookupBase):
    pass


class WorkOrderStatusLookupUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    abbreviation: Optional[str] = Field(None, max_length=10)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class WorkOrderStatusLookupResponse(WorkOrderStatusLookupBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SalesTypeLookupBase(BaseModel):
    name: str = Field(..., max_length=50)
    abbreviation: str = Field(..., max_length=10)
    description: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class SalesTypeLookupCreate(SalesTypeLookupBase):
    pass


class SalesTypeLookupUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    abbreviation: Optional[str] = Field(None, max_length=10)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class SalesTypeLookupResponse(SalesTypeLookupBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True