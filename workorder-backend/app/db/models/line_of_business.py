"""app.db.models.line_of_business.models.py"""

import uuid
from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class LineOfBusiness(Base):
    __tablename__ = "line_of_businesses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    division_name = Column(String(255), nullable=False)
    division_abbreviation = Column(String(50), nullable=True)
    lob_name = Column(String(255), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    # A line of business can belong to many branches (many-to-one from Branch to LineOfBusiness)
    branches = relationship("Branch", back_populates="line_of_business")

    def __repr__(self) -> str:
        return f"<LineOfBusiness(id={self.id}, lob_name={self.lob_name!r}, division_name={self.division_name!r})>"