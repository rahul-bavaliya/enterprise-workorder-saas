# app/api/v1/endpoints/work_order_status.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.work_order import WorkOrderStatusLookupCreate, WorkOrderStatusLookupResponse, WorkOrderStatusLookupUpdate
from app.api.v1.services.work_order import WorkOrderStatusLookupService

router = APIRouter()


@router.post("/", response_model=WorkOrderStatusLookupResponse, status_code=status.HTTP_201_CREATED)
def create_work_order_status(
    *,
    status_in: WorkOrderStatusLookupCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderStatusLookupResponse:
    """
    Create a new work order status.
    """
    service = WorkOrderStatusLookupService(db)
    return service.create(obj_in=status_in)


@router.get("/", response_model=List[WorkOrderStatusLookupResponse])
def read_work_order_statuses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[WorkOrderStatusLookupResponse]:
    """
    Retrieve work order statuses.
    """
    service = WorkOrderStatusLookupService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{status_id}", response_model=WorkOrderStatusLookupResponse)
def read_work_order_status(
    *,
    status_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderStatusLookupResponse:
    """
    Get a specific work order status by id.
    """
    service = WorkOrderStatusLookupService(db)
    status = service.get(id=status_id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order status not found",
        )
    return status


@router.patch("/{status_id}", response_model=WorkOrderStatusLookupResponse)
def update_work_order_status(
    *,
    status_id: UUID,
    status_in: WorkOrderStatusLookupUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderStatusLookupResponse:
    """
    Update a work order status.
    """
    service = WorkOrderStatusLookupService(db)
    status = service.get(id=status_id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order status not found",
        )
    return service.update(db_obj=status, obj_in=status_in)


@router.delete("/{status_id}", response_model=WorkOrderStatusLookupResponse)
def delete_work_order_status(
    *,
    status_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> WorkOrderStatusLookupResponse:
    """
    Delete a work order status.
    """
    service = WorkOrderStatusLookupService(db)
    status = service.get(id=status_id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order status not found",
        )
    return service.remove(id=status_id)