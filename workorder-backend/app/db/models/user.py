"""app.db.models.user.models.py"""

import uuid
from sqlalchemy import Column, String, DateTime, func, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DISPATCHER = "dispatcher"
    TECHNICIAN = "technician"
    VIEWER = "viewer"
    SERVICE_MANAGER = "service_manager"
    SERVICE_WRITER = "service_writer"
    BRANCH_MANAGER = "branch_manager"
    FOREMAN = "foreman"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), nullable=False, default=UserRole.TECHNICIAN)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email!r}, role={self.role!r})>"