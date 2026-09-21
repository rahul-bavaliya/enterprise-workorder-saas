"""app.db.models.branch.models.py"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Column,
    Identity,
    Integer,
    Numeric,
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
from app.db.models.line_of_business import LineOfBusiness


class Branch(Base):
    __tablename__ = "branches"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Business Relationship
    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False
    )

    # Branch Manager Relationship
    branch_manager_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    # Branch Details
    name = Column(String(255), nullable=False)
    number = Column(
        Integer,
        Identity(start=10001, always=False),
        nullable=False,
        unique=True,
    )
    lob_id = Column(
        UUID(as_uuid=True),
        ForeignKey("line_of_businesses.id"),
        nullable=False,
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

    # Active Status
    is_active = Column(Boolean, nullable=False, default=True)

    # Audit Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        ),  # Populates on the Python object immediately
        server_default=func.now(),  # Ensures DB fallback
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),  # Punches new time on update
        nullable=False,
    )

    # Relationships
    business = relationship("Business", back_populates="branches")
    branch_manager = relationship("User", foreign_keys=[branch_manager_id])
    line_of_business = relationship("LineOfBusiness", back_populates="branches")
    departments = relationship("Department", back_populates="branch")

    # Database Performance Optimization Indexes
    __table_args__ = (
        Index("ix_branches_email", "email"),
        Index("ix_branches_is_active", "is_active"),
        Index("ix_branches_name", "name"),
        Index("ix_branches_business_id", "business_id"),
        Index("ix_branches_branch_manager_id", "branch_manager_id"),
    )

    def __repr__(self) -> str:
        return f"<Branch(id={self.id}, name={self.name!r}, number={self.number})>"
