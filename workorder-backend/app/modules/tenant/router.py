"""app/modules/tenant/router.py"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.modules.tenant.models import Tenant
from app.modules.tenant.schemas import TenantCreate, TenantResponse

router = APIRouter(prefix="/tenants", tags=["Tenants & Multi-Tenancy"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(tenant_in: TenantCreate, db: AsyncSession = Depends(get_db)):
    # Check if tenant name or schema already exists
    result = await db.execute(select(Tenant).where(Tenant.name == tenant_in.name))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant with this name already exists.",
        )

    new_tenant = Tenant(name=tenant_in.name, schema_name=tenant_in.schema_name)
    db.add(new_tenant)
    await db.commit()
    await db.refresh(new_tenant)
    return new_tenant


@router.get("/", response_model=list[TenantResponse])
async def list_tenants(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenant))
    return result.scalars().all()
