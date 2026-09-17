"""app/modules/work_order/schemas.py"""

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.modules.work_order.models import (
    AssetCategory,
    WorkOrderStatus,
    WorkOrderPriority,
)


class AssetCreate(BaseModel):
    tenant_id: UUID
    name: str
    category: AssetCategory
    serial_number: Optional[str] = None
    location: Optional[str] = None


class AssetResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    category: AssetCategory
    serial_number: Optional[str]
    location: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class WorkOrderCreate(BaseModel):
    tenant_id: UUID
    asset_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM


class WorkOrderResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    asset_id: Optional[UUID]
    title: str
    description: Optional[str]
    status: WorkOrderStatus
    priority: WorkOrderPriority
    assigned_technician_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
