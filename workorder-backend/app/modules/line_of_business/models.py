import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class LineOfBusiness(Base):
    # Fixed Table Name: Grammatically correct pluralization
    __tablename__ = "line_of_businesses"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Line of Business Details
    division_name = Column(String(255), nullable=False)
    division_abbreviation = Column(String(50), nullable=True)
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

    # Relationships (Make sure the matching relationship is added on your Branch model)
    branches = relationship("Branch", back_populates="line_of_business")

    # Database Performance Optimization Indexes
    __table_args__ = (
        Index("ix_line_of_businesses_division_name", "division_name"),
        Index("ix_line_of_businesses_lob_name", "lob_name"),
    )
