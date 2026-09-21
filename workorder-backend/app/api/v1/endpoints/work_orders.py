# app/api/v1/endpoints/work_orders.py
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderResponse,
    WorkOrderUpdate,
)
from app.api.v1.services.work_order import WorkOrderService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[WorkOrderResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_work_order(
    *,
    work_order_in: WorkOrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderResponse]:
    """
    Create a new work order.
    """
    service = WorkOrderService(db)
    work_order = await service.create(obj_in=work_order_in)
    return ResponseEnvelope[WorkOrderResponse].ok(
        data=WorkOrderResponse.model_validate(work_order),
        message="Work order created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[WorkOrderResponse]])
async def read_work_orders(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = Query(100, ge=1, le=100),
    customer_id: Optional[UUID] = Query(None, description="Filter by customer ID"),
    asset_id: Optional[UUID] = Query(None, description="Filter by asset ID"),
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[WorkOrderResponse]]:
    """
    Retrieve work orders.
    """
    service = WorkOrderService(db)
    if customer_id:
        work_orders = await service.get_multi_by_customer(
            customer_id=customer_id, skip=skip, limit=limit
        )
    elif asset_id:
        work_orders = await service.get_multi_by_asset(
            asset_id=asset_id, skip=skip, limit=limit
        )
    else:
        work_orders = await service.get_multi(skip=skip, limit=limit)

    work_order_responses = [WorkOrderResponse.model_validate(wo) for wo in work_orders]
    return ResponseEnvelope[List[WorkOrderResponse]].ok(
        data=work_order_responses, message="Work orders retrieved successfully"
    )


@router.get("/{work_order_id}", response_model=ResponseEnvelope[WorkOrderResponse])
async def read_work_order(
    *,
    work_order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderResponse]:
    """
    Get a specific work order by id.
    """
    service = WorkOrderService(db)
    work_order = await service.get(id=work_order_id)
    if not work_order:
        raise NotFoundException(message="Work order not found")
    return ResponseEnvelope[WorkOrderResponse].ok(
        data=WorkOrderResponse.model_validate(work_order),
        message="Work order retrieved successfully",
    )


@router.patch("/{work_order_id}", response_model=ResponseEnvelope[WorkOrderResponse])
async def update_work_order(
    *,
    work_order_id: UUID,
    work_order_in: WorkOrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderResponse]:
    """
    Update a work order.
    """
    service = WorkOrderService(db)
    work_order = await service.get(id=work_order_id)
    if not work_order:
        raise NotFoundException(message="Work order not found")
    updated_work_order = await service.update(db_obj=work_order, obj_in=work_order_in)
    return ResponseEnvelope[WorkOrderResponse].ok(
        data=WorkOrderResponse.model_validate(updated_work_order),
        message="Work order updated successfully",
    )


@router.delete("/{work_order_id}", response_model=ResponseEnvelope[WorkOrderResponse])
async def delete_work_order(
    *,
    work_order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderResponse]:
    """
    Delete a work order.
    """
    service = WorkOrderService(db)
    work_order = await service.get(id=work_order_id)
    if not work_order:
        raise NotFoundException(message="Work order not found")
    deleted_work_order = await service.remove(id=work_order_id)
    return ResponseEnvelope[
        (
            ResponseEnvelope[WorkOrderResponse].ok(
                data=WorkOrderResponse.model_validate(deleted_work_order),
                message="Work order deleted successfully",
            )
            if False
            else ResponseEnvelope[WorkOrderResponse].ok(
                data=WorkOrderResponse.model_validate(deleted_work_order),
                message="Work order deleted successfully",
            )
        )
    ]  # Cleaned block below
