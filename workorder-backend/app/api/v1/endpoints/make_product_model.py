# app/api/v1/endpoints/make_product_model.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.make_product_model import (
    MakeProductModelCreate,
    MakeProductModelResponse,
    MakeProductModelUpdate,
)
from app.api.v1.services.make_product_model import MakeProductModelService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[MakeProductModelResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_make_product_model(
    *,
    model_in: MakeProductModelCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[MakeProductModelResponse]:
    """
    Create a new make product model.
    """
    service = MakeProductModelService(db)
    model = await service.create(obj_in=model_in)
    return ResponseEnvelope[MakeProductModelResponse].ok(
        data=MakeProductModelResponse.model_validate(model),
        message="Make product model created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[MakeProductModelResponse]])
async def read_make_product_models(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[MakeProductModelResponse]]:
    """
    Retrieve make product models.
    """
    service = MakeProductModelService(db)
    models = await service.get_multi(skip=skip, limit=limit)
    model_responses = [MakeProductModelResponse.model_validate(m) for m in models]
    return ResponseEnvelope[List[MakeProductModelResponse]].ok(
        data=model_responses, message="Make product models retrieved successfully"
    )


@router.get("/{model_id}", response_model=ResponseEnvelope[MakeProductModelResponse])
async def read_make_product_model(
    *,
    model_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[MakeProductModelResponse]:
    """
    Get a specific make product model by id.
    """
    service = MakeProductModelService(db)
    model = await service.get(id=model_id)
    if not model:
        raise NotFoundException(message="Make product model not found")
    return ResponseEnvelope[MakeProductModelResponse].ok(
        data=MakeProductModelResponse.model_validate(model),
        message="Make product model retrieved successfully",
    )


@router.patch("/{model_id}", response_model=ResponseEnvelope[MakeProductModelResponse])
async def update_make_product_model(
    *,
    model_id: UUID,
    model_in: MakeProductModelUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[MakeProductModelResponse]:
    """
    Update a make product model.
    """
    service = MakeProductModelService(db)
    model = await service.get(id=model_id)
    if not model:
        raise NotFoundException(message="Make product model not found")
    updated_model = await service.update(db_obj=model, obj_in=model_in)
    return ResponseEnvelope[MakeProductModelResponse].ok(
        data=MakeProductModelResponse.model_validate(updated_model),
        message="Make product model updated successfully",
    )


@router.delete("/{model_id}", response_model=ResponseEnvelope[MakeProductModelResponse])
async def delete_make_product_model(
    *,
    model_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[MakeProductModelResponse]:
    """
    Delete a make product model.
    """
    service = MakeProductModelService(db)
    model = await service.get(id=model_id)
    if not model:
        raise NotFoundException(message="Make product model not found")
    deleted_model = await service.remove(id=model_id)
    return ResponseEnvelope[MakeProductModelResponse].ok(
        data=MakeProductModelResponse.model_validate(deleted_model),
        message="Make product model deleted successfully",
    )
