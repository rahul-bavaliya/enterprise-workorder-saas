"""app.modules.branch.models.py"""

from datetime import datetime, timezone
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

    # Foreign Key pointing to Line of Business
    lob_id = Column(
        UUID(as_uuid=True),
        ForeignKey("line_of_businesses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

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
    line_of_business = relationship("LineOfBusiness", back_populates="branches")

    # Database Performance Optimization Indexes
    __table_args__ = (
        Index("ix_branches_email", "email"),
        Index("ix_branches_is_active", "is_active"),
        Index(
            "ix_branches_name", "name", unique=True
        ),  # Enforces unique name at DB level
    )
