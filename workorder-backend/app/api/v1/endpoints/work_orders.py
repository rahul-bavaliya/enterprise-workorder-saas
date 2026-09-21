# app/api/v1/endpoints/work_orders.py
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.work_order import WorkOrderCreate, WorkOrderResponse, WorkOrderUpdate
from app.api.v1.services.work_order import WorkOrderService

router = APIRouter()


@router.post("/", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
def create_work_order(
    *,
    work_order_in: WorkOrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderResponse:
    """
    Create a new work order.
    """
    service = WorkOrderService(db)
    return service.create(obj_in=work_order_in)


@router.get("/", response_model=List[WorkOrderResponse])
def read_work_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(100, ge=1, le=100),
    customer_id: Optional[UUID] = Query(None, description="Filter by customer ID"),
    asset_id: Optional[UUID] = Query(None, description="Filter by asset ID"),
    current_user = Depends(get_current_active_user)
) -> List[WorkOrderResponse]:
    """
    Retrieve work orders.
    """
    service = WorkOrderService(db)
    if customer_id:
        return service.get_multi_by_customer(customer_id=customer_id, skip=skip, limit=limit)
    if asset_id:
        return service.get_multi_by_asset(asset_id=asset_id, skip=skip, limit=limit)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
def read_work_order(
    *,
    work_order_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderResponse:
    """
    Get a specific work order by id.
    """
    service = WorkOrderService(db)
    work_order = service.get(id=work_order_id)
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order not found",
        )
    return work_order


@router.patch("/{work_order_id}", response_model=WorkOrderResponse)
def update_work_order(
    *,
    work_order_id: UUID,
    work_order_in: WorkOrderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderResponse:
    """
    Update a work order.
    """
    service = WorkOrderService(db)
    work_order = service.get(id=work_order_id)
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order not found",
        )
    return service.update(db_obj=work_order, obj_in=work_order_in)


@router.delete("/{work_order_id}", response_model=WorkOrderResponse)
def delete_work_order(
    *,
    work_order_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderResponse:
    """
    Delete a work order.
    """
    service = WorkOrderService(db)
    work_order = service.get(id=work_order_id)
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order not found",
        )
    return service.remove(id=work_order_id)