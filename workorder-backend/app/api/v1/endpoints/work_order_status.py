# app/api/v1/endpoints/work_order_status.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.work_order import WorkOrderStatusLookupCreate, WorkOrderStatusLookupResponse, WorkOrderStatusLookupUpdate
from app.api.v1.services.work_order import WorkOrderStatusLookupService

router = APIRouter()


@router.post("/", response_model=ResponseEnvelope[WorkOrderStatusLookupResponse], status_code=status.HTTP_201_CREATED)
async def create_work_order_status(
    *,
    status_in: WorkOrderStatusLookupCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderStatusLookupResponse]:
    """
    Create a new work order status.
    """
    service = WorkOrderStatusLookupService(db)
    work_order_status = await service.create(obj_in=status_in)
    return ResponseEnvelope[WorkOrderStatusLookupResponse].ok(
        data=WorkOrderStatusLookupResponse.model_validate(work_order_status),
        message="Work order status created successfully"
    )


@router.get("/", response_model=ResponseEnvelope[List[WorkOrderStatusLookupResponse]])
async def read_work_order_statuses(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> ResponseEnvelope[List[WorkOrderStatusLookupResponse]]:
    """
    Retrieve work order statuses.
    """
    service = WorkOrderStatusLookupService(db)
    work_order_statuses = await service.get_multi(skip=skip, limit=limit)
    status_responses = [WorkOrderStatusLookupResponse.model_validate(s) for s in work_order_statuses]
    return ResponseEnvelope[List[WorkOrderStatusLookupResponse]].ok(
        data=status_responses,
        message="Work order statuses retrieved successfully"
    )


@router.get("/{status_id}", response_model=ResponseEnvelope[WorkOrderStatusLookupResponse])
async def read_work_order_status(
    *,
    status_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderStatusLookupResponse]:
    """
    Get a specific work order status by id.
    """
    service = WorkOrderStatusLookupService(db)
    work_order_status = await service.get(id=status_id)
    if not work_order_status:
        raise NotFoundException(message="Work order status not found")
    return ResponseEnvelope[WorkOrderStatusLookupResponse].ok(
        data=WorkOrderStatusLookupResponse.model_validate(work_order_status),
        message="Work order status retrieved successfully"
    )


@router.patch("/{status_id}", response_model=ResponseEnvelope[WorkOrderStatusLookupResponse])
async def update_work_order_status(
    *,
    status_id: UUID,
    status_in: WorkOrderStatusLookupUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderStatusLookupResponse]:
    """
    Update a work order status.
    """
    service = WorkOrderStatusLookupService(db)
    work_order_status = await service.get(id=status_id)
    if not work_order_status:
        raise NotFoundException(message="Work order status not found")
    updated_status = await service.update(db_obj=work_order_status, obj_in=status_in)
    return ResponseEnvelope[WorkOrderStatusLookupResponse].ok(
        data=WorkOrderStatusLookupResponse.model_validate(updated_status),
        message="Work order status updated successfully"
    )


@router.delete("/{status_id}", response_model=ResponseEnvelope[WorkOrderStatusLookupResponse])
async def delete_work_order_status(
    *,
    status_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> ResponseEnvelope[ResponseEnvelope[WorkOrderStatusLookupResponse].ok]: # handled below as clean ResponseEnvelope