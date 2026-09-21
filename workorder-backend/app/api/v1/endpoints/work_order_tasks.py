# app/api/v1/endpoints/work_order_tasks.py
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.work_order import (
    WorkOrderTaskCreate,
    WorkOrderTaskResponse,
    WorkOrderTaskUpdate,
)
from app.api.v1.services.work_order import WorkOrderTaskService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[WorkOrderTaskResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_work_order_task(
    *,
    task_in: WorkOrderTaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderTaskResponse]:
    """
    Create a new work order task.
    """
    service = WorkOrderTaskService(db)
    task = await service.create(obj_in=task_in)
    return ResponseEnvelope[WorkOrderTaskResponse].ok(
        data=WorkOrderTaskResponse.model_validate(task),
        message="Work order task created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[WorkOrderTaskResponse]])
async def read_work_order_tasks(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    work_order_id: Optional[UUID] = Query(None, description="Filter by work order ID"),
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[WorkOrderTaskResponse]]:
    """
    Retrieve work order tasks.
    """
    service = WorkOrderTaskService(db)
    if work_order_id:
        tasks = await service.get_multi_by_work_order(
            work_order_id=work_order_id, skip=skip, limit=limit
        )
    else:
        tasks = await service.get_multi(skip=skip, limit=limit)

    task_responses = [WorkOrderTaskResponse.model_validate(t) for t in tasks]
    return ResponseEnvelope[List[WorkOrderTaskResponse]].ok(
        data=task_responses, message="Work order tasks retrieved successfully"
    )


@router.get("/{task_id}", response_model=ResponseEnvelope[WorkOrderTaskResponse])
async def read_work_order_task(
    *,
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderTaskResponse]:
    """
    Get a specific work order task by id.
    """
    service = WorkOrderTaskService(db)
    task = await service.get(id=task_id)
    if not task:
        raise NotFoundException(message="Work order task not found")
    return ResponseEnvelope[WorkOrderTaskResponse].ok(
        data=WorkOrderTaskResponse.model_validate(task),
        message="Work order task retrieved successfully",
    )


@router.patch("/{task_id}", response_model=ResponseEnvelope[WorkOrderTaskResponse])
async def update_work_order_task(
    *,
    task_id: UUID,
    task_in: WorkOrderTaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderTaskResponse]:
    """
    Update a work order task.
    """
    service = WorkOrderTaskService(db)
    task = await service.get(id=task_id)
    if not task:
        raise NotFoundException(message="Work order task not found")
    updated_task = await service.update(db_obj=task, obj_in=task_in)
    return ResponseEnvelope[WorkOrderTaskResponse].ok(
        data=WorkOrderTaskResponse.model_validate(updated_task),
        message="Work order task updated successfully",
    )


@router.delete("/{task_id}", response_model=ResponseEnvelope[WorkOrderTaskResponse])
async def delete_work_order_task(
    *,
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[WorkOrderTaskResponse]:
    """
    Delete a work order task.
    """
    service = WorkOrderTaskService(db)
    task = await service.get(id=task_id)
    if not task:
        raise NotFoundException(message="Work order task not found")
    deleted_task = await service.remove(id=task_id)
    return ResponseEnvelope[WorkOrderTaskResponse].ok(
        data=WorkOrderTaskResponse.model_validate(deleted_task),
        message="Work order task deleted successfully",
    )
