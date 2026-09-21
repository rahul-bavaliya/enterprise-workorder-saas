"""app.db.models.department.models.py"""

import uuid
from sqlalchemy import Column, String, DateTime, Boolean, func, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    branch_id = Column(
        UUID(as_uuid=True),
        ForeignKey("branches.id"),
        nullable=False
    )
    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    branch = relationship("Branch", back_populates="departments")
    manager = relationship("User", foreign_keys=[manager_id])

    def __repr__(self) -> str:
        return f"<Department(id={self.id}, name={self.name!r})>"