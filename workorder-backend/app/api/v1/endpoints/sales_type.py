# app/api/v1/endpoints/sales_type.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.work_order import (
    SalesTypeLookupCreate,
    SalesTypeLookupResponse,
    SalesTypeLookupUpdate,
)
from app.api.v1.services.work_order import SalesTypeLookupService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[SalesTypeLookupResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_sales_type(
    *,
    sales_type_in: SalesTypeLookupCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[SalesTypeLookupResponse]:
    """
    Create a new sales type.
    """
    service = SalesTypeLookupService(db)
    sales_type = await service.create(obj_in=sales_type_in)
    return ResponseEnvelope[SalesTypeLookupResponse].ok(
        data=SalesTypeLookupResponse.model_validate(sales_type),
        message="Sales type created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[SalesTypeLookupResponse]])
async def read_sales_types(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[SalesTypeLookupResponse]]:
    """
    Retrieve sales types.
    """
    service = SalesTypeLookupService(db)
    sales_types = await service.get_multi(skip=skip, limit=limit)
    sales_type_responses = [
        SalesTypeLookupResponse.model_validate(st) for st in sales_types
    ]
    return ResponseEnvelope[List[SalesTypeLookupResponse]].ok(
        data=sales_type_responses, message="Sales types retrieved successfully"
    )


@router.get(
    "/{sales_type_id}", response_model=ResponseEnvelope[SalesTypeLookupResponse]
)
async def read_sales_type(
    *,
    sales_type_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[SalesTypeLookupResponse]:
    """
    Get a specific sales type by id.
    """
    service = SalesTypeLookupService(db)
    sales_type = await service.get(id=sales_type_id)
    if not sales_type:
        raise NotFoundException(message="Sales type not found")
    return ResponseEnvelope[SalesTypeLookupResponse].ok(
        data=SalesTypeLookupResponse.model_validate(sales_type),
        message="Sales type retrieved successfully",
    )


@router.patch(
    "/{sales_type_id}", response_model=ResponseEnvelope[SalesTypeLookupResponse]
)
async def update_sales_type(
    *,
    sales_type_id: UUID,
    sales_type_in: SalesTypeLookupUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[SalesTypeLookupResponse]:
    """
    Update a sales type.
    """
    service = SalesTypeLookupService(db)
    sales_type = await service.get(id=sales_type_id)
    if not sales_type:
        raise NotFoundException(message="Sales type not found")
    updated_sales_type = await service.update(db_obj=sales_type, obj_in=sales_type_in)
    return ResponseEnvelope[SalesTypeLookupResponse].ok(
        data=SalesTypeLookupResponse.model_validate(updated_sales_type),
        message="Sales type updated successfully",
    )


@router.delete(
    "/{sales_type_id}", response_model=ResponseEnvelope[SalesTypeLookupResponse]
)
async def delete_sales_type(
    *,
    sales_type_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[SalesTypeLookupResponse]:
    """
    Delete a sales type.
    """
    service = SalesTypeLookupService(db)
    sales_type = await service.get(id=sales_type_id)
    if not sales_type:
        raise NotFoundException(message="Sales type not found")
    deleted_sales_type = await service.remove(id=sales_type_id)
    return ResponseEnvelope[SalesTypeLookupResponse].ok(
        data=SalesTypeLookupResponse.model_validate(deleted_sales_type),
        message="Sales type deleted successfully",
    )
