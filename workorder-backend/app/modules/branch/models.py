"""app.modules.branch.models.py"""

import uuid
from sqlalchemy import (
    Column,
    Identity,
    Integer,
    Numeric,
    Sequence,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Branch(Base):
    __tablename__ = "branches"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Multi-Tenant Isolation (Added back explicitly to support your BranchCreate schema context)
    # tenant_id = Column(
    #     UUID(as_uuid=True),
    #     ForeignKey("tenants.id", ondelete="CASCADE"),
    #     nullable=False,
    # )

    # Branch Details
    name = Column(String(255), nullable=False)
    number = Column(
        Integer,
        Identity(start=10001, always=False),
        nullable=False,
        unique=True,
    )

    # Branch Location Details
    address1 = Column(String(500), nullable=True)
    address2 = Column(String(500), nullable=True)
    city = Column(String(255), nullable=False)
    postal_code = Column(String(20), nullable=False)
    province = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    latitude = Column(Numeric(precision=9, scale=6), nullable=True)
    longitude = Column(Numeric(precision=9, scale=6), nullable=True)
    region = Column(String(255), nullable=True)

    # Branch Contact Details
    # Increased to String(15) to allow standard E.164 phone formats safely while staying strict
    phone = Column(String(15), nullable=True)
    email = Column(String(255), nullable=True)
    website_url = Column(String(500), nullable=True)
    contact_person = Column(String(255), nullable=True)

    # Division Details
    division_name = Column(String(255), nullable=False)
    lob_name = Column(String(255), nullable=False)

    # Active Status
    is_active = Column(Boolean, nullable=False, default=True)

    # Audit Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    # tenant = relationship("Tenant", back_populates="branches")

    # Database Performance Optimization Indexes
    __table_args__ = (
        Index("ix_branches_email", "email"),
        Index("ix_branches_is_active", "is_active"),
        Index("ix_branches_name", "name"),
    )

    def __repr__(self) -> str:
        return f"<Branch(id={self.id}, name={self.name!r}, number={self.number})>"
