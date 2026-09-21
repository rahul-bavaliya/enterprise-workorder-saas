# app/api/v1/endpoints/department.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.api.v1.services.department import DepartmentService

router = APIRouter()


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    *,
    department_in: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> DepartmentResponse:
    """
    Create a new department.
    """
    service = DepartmentService(db)
    return service.create(obj_in=department_in)


@router.get("/", response_model=List[DepartmentResponse])
def read_departments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[DepartmentResponse]:
    """
    Retrieve departments.
    """
    service = DepartmentService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{department_id}", response_model=DepartmentResponse)
def read_department(
    *,
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> DepartmentResponse:
    """
    Get a specific department by id.
    """
    service = DepartmentService(db)
    department = service.get(id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    return department


@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(
    *,
    department_id: UUID,
    department_in: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> DepartmentResponse:
    """
    Update a department.
    """
    service = DepartmentService(db)
    department = service.get(id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    return service.update(db_obj=department, obj_in=department_in)


@router.delete("/{department_id}", response_model=DepartmentResponse)
def delete_department(
    *,
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> DepartmentResponse:
    """
    Delete a department.
    """
    service = DepartmentService(db)
    department = service.get(id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    return service.remove(id=department_id)