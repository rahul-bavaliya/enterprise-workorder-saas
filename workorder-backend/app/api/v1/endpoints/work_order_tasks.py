# app/api/v1/endpoints/work_order_tasks.py
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.work_order import WorkOrderTaskCreate, WorkOrderTaskResponse, WorkOrderTaskUpdate
from app.api.v1.services.work_order import WorkOrderTaskService

router = APIRouter()


@router.post("/", response_model=WorkOrderTaskResponse, status_code=status.HTTP_201_CREATED)
def create_work_order_task(
    *,
    task_in: WorkOrderTaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderTaskResponse:
    """
    Create a new work order task.
    """
    service = WorkOrderTaskService(db)
    return service.create(obj_in=task_in)


@router.get("/", response_model=List[WorkOrderTaskResponse])
def read_work_order_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    work_order_id: Optional[UUID] = Query(None, description="Filter by work order ID"),
    current_user = Depends(get_current_active_user)
) -> List[WorkOrderTaskResponse]:
    """
    Retrieve work order tasks.
    """
    service = WorkOrderTaskService(db)
    if work_order_id:
        return service.get_multi_by_work_order(work_order_id=work_order_id, skip=skip, limit=limit)
    return []


@router.get("/{task_id}", response_model=WorkOrderTaskResponse)
def read_work_order_task(
    *,
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderTaskResponse:
    """
    Get a specific work order task by id.
    """
    service = WorkOrderTaskService(db)
    task = service.get(id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order task not found",
        )
    return task


@router.patch("/{task_id}", response_model=WorkOrderTaskResponse)
def update_work_order_task(
    *,
    task_id: UUID,
    task_in: WorkOrderTaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderTaskResponse:
    """
    Update a work order task.
    """
    service = WorkOrderTaskService(db)
    task = service.get(id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order task not found",
        )
    return service.update(db_obj=task, obj_in=task_in)


@router.delete("/{task_id}", response_model=WorkOrderTaskResponse)
def delete_work_order_task(
    *,
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderTaskResponse:
    """
    Delete a work order task.
    """
    service = WorkOrderTaskService(db)
    task = service.get(id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order task not found",
        )
    return service.remove(id=task_id)