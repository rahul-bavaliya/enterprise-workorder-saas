# app/api/v1/endpoints/department.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.api.v1.services.department import DepartmentService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[DepartmentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    *,
    department_in: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[DepartmentResponse]:
    """
    Create a new department.
    """
    service = DepartmentService(db)
    department = await service.create(obj_in=department_in)
    return ResponseEnvelope[DepartmentResponse].ok(
        data=DepartmentResponse.model_validate(department),
        message="Department created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[DepartmentResponse]])
async def read_departments(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[DepartmentResponse]]:
    """
    Retrieve departments.
    """
    service = DepartmentService(db)
    departments = await service.get_multi(skip=skip, limit=limit)
    department_responses = [DepartmentResponse.model_validate(d) for d in departments]
    return ResponseEnvelope[List[DepartmentResponse]].ok(
        data=department_responses, message="Departments retrieved successfully"
    )


@router.get("/{department_id}", response_model=ResponseEnvelope[DepartmentResponse])
async def read_department(
    *,
    department_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[DepartmentResponse]:
    """
    Get a specific department by id.
    """
    service = DepartmentService(db)
    department = await service.get(id=department_id)
    if not department:
        raise NotFoundException(message="Department not found")
    return ResponseEnvelope[DepartmentResponse].ok(
        data=DepartmentResponse.model_validate(department),
        message="Department retrieved successfully",
    )


@router.patch("/{department_id}", response_model=ResponseEnvelope[DepartmentResponse])
async def update_department(
    *,
    department_id: UUID,
    department_in: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[DepartmentResponse]:
    """
    Update a department.
    """
    service = DepartmentService(db)
    department = await service.get(id=department_id)
    if not department:
        raise NotFoundException(message="Department not found")
    updated_department = await service.update(db_obj=department, obj_in=department_in)
    return ResponseEnvelope[DepartmentResponse].ok(
        data=DepartmentResponse.model_validate(updated_department),
        message="Department updated successfully",
    )


@router.delete("/{department_id}", response_model=ResponseEnvelope[DepartmentResponse])
async def delete_department(
    *,
    department_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[DepartmentResponse]:
    """
    Delete a department.
    """
    service = DepartmentService(db)
    department = await service.get(id=department_id)
    if not department:
        raise NotFoundException(message="Department not found")
    deleted_department = await service.remove(id=department_id)
    return ResponseEnvelope[DepartmentResponse].ok(
        data=DepartmentResponse.model_validate(deleted_department),
        message="Department deleted successfully",
    )
