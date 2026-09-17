"""app/modules/work_order/models.py"""

import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class AssetCategory(str, enum.Enum):
    HVAC = "hvac"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    MACHINERY = "machinery"
    IT_INFRASTRUCTURE = "it_infrastructure"


class WorkOrderStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    TRIAGED = "triaged"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WorkOrderPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    category = Column(Enum(AssetCategory), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    work_orders = relationship(
        "WorkOrder", back_populates="asset", cascade="all, delete-orphan"
    )


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    asset_id = Column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="SET NULL"), nullable=True
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(WorkOrderStatus), nullable=False, default=WorkOrderStatus.SUBMITTED
    )
    priority = Column(
        Enum(WorkOrderPriority), nullable=False, default=WorkOrderPriority.MEDIUM
    )
    assigned_technician_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    asset = relationship("Asset", back_populates="work_orders")
    tasks = relationship(
        "WorkOrderTask", back_populates="work_order", cascade="all, delete-orphan"
    )


class WorkOrderTask(Base):
    __tablename__ = "work_order_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("work_orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)

    work_order = relationship("WorkOrder", back_populates="tasks")
