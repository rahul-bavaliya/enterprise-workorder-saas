"""app/modules/tenant/schemas.py"""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from app.modules.tenant.models import UserRole


class TenantCreate(BaseModel):
    name: str
    schema_name: str


class TenantResponse(BaseModel):
    id: UUID
    name: str
    schema_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.TECHNICIAN


class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True
