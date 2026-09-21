from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Identity,
    Integer,
    Numeric,
    String,
    Boolean,
    DateTime,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Branch(Base):
    __tablename__ = "branches"

    # Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    # Branch Details
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    number: Mapped[int] = mapped_column(
        Integer,
        Identity(start=10001, always=False),
        nullable=False,
        unique=True,
    )

    # Branch Location Details
    address1: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address2: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    province: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    region: Mapped[str | None] = mapped_column(String(255), nullable=True)

    latitude: Mapped[float | None] = mapped_column(
        Numeric(precision=9, scale=6), nullable=True
    )
    longitude: Mapped[float | None] = mapped_column(
        Numeric(precision=9, scale=6), nullable=True
    )

    join_key: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
        index=True,
    )

    # Branch Contact Details
    phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    contact_person: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Division & Line of Business Details
    division_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lob_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Active Status
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, index=True
    )

    # Audit Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=None,
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Advanced Composite Indexes for Multi-tenant/Location Filtering
    __table_args__ = (
        Index("ix_branches_location_composite", "country", "province", "city"),
        Index("ix_branches_business_div", "lob_name", "division_name"),
    )

    def __repr__(self) -> str:
        return f"<Branch(id={self.id}, name={self.name!r}, number={self.number})>"
