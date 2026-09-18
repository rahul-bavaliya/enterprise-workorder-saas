# app/modules/work_order/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.database import get_db
from app.modules.work_order.models import Asset, WorkOrder
from app.modules.work_order.schemas import (
    AssetCreate,
    AssetResponse,
    WorkOrderCreate,
    WorkOrderResponse,
)

router = APIRouter(prefix="/work-orders", tags=["Work Orders & Assets"])


@router.post(
    "/assets/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED
)
async def create_asset(asset_in: AssetCreate, db: AsyncSession = Depends(get_db)):
    new_asset = Asset(**asset_in.model_dump())
    db.add(new_asset)
    await db.commit()
    await db.refresh(new_asset)
    return new_asset


@router.post("/", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_work_order(wo_in: WorkOrderCreate, db: AsyncSession = Depends(get_db)):
    new_wo = WorkOrder(**wo_in.model_dump())
    db.add(new_wo)
    await db.commit()
    await db.refresh(new_wo)
    return new_wo


@router.get("/", response_model=list[WorkOrderResponse])
async def list_work_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WorkOrder))
    return result.scalars().all()
