"""app.db.models.work_order.models.py"""

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


class WorkOrderPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkOrderStatusLookup(Base):
    __tablename__ = "work_order_status_lookup"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)  # e.g., "submitted"
    abbreviation = Column(String(10), nullable=False, unique=True)  # e.g., "SUB"
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SalesTypeLookup(Base):
    __tablename__ = "sales_type_lookup"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)  # e.g., "Installation"
    abbreviation = Column(String(10), nullable=False, unique=True)  # e.g., "INST"
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False
    )
    name = Column(String(255), nullable=False)
    category = Column(Enum(AssetCategory), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="assets")
    work_orders = relationship(
        "WorkOrder", back_populates="asset", cascade="all, delete-orphan"
    )


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False
    )
    asset_id = Column(
        UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False
    )
    status_id = Column(
        UUID(as_uuid=True), ForeignKey("work_order_status_lookup.id"), nullable=False
    )
    priority = Column(
        Enum(WorkOrderPriority), nullable=False, default=WorkOrderPriority.MEDIUM
    )
    sales_type_id = Column(
        UUID(as_uuid=True), ForeignKey("sales_type_lookup.id"), nullable=False
    )
    assigned_technician_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    customer = relationship("Customer")
    asset = relationship("Asset", back_populates="work_orders")
    status = relationship("WorkOrderStatusLookup")
    sales_type = relationship("SalesTypeLookup")
    tasks = relationship("WorkOrderTask", back_populates="work_order", cascade="all, delete-orphan")


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