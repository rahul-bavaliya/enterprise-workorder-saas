# app/api/v1/endpoints/line_of_business.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.line_of_business import (
    LineOfBusinessCreate,
    LineOfBusinessResponse,
    LineOfBusinessUpdate,
)
from app.api.v1.services.line_of_business import LineOfBusinessService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[LineOfBusinessResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_line_of_business(
    *,
    lob_in: LineOfBusinessCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[LineOfBusinessResponse]:
    """
    Create a new line of business.
    """
    service = LineOfBusinessService(db)
    lob = await service.create(obj_in=lob_in)
    return ResponseEnvelope[LineOfBusinessResponse].ok(
        data=LineOfBusinessResponse.model_validate(lob),
        message="Line of business created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[LineOfBusinessResponse]])
async def read_lines_of_business(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[LineOfBusinessResponse]]:
    """
    Retrieve lines of business.
    """
    service = LineOfBusinessService(db)
    lobs = await service.get_multi(skip=skip, limit=limit)
    lob_responses = [LineOfBusinessResponse.model_validate(lob) for lob in lobs]
    return ResponseEnvelope[List[LineOfBusinessResponse]].ok(
        data=lob_responses, message="Lines of business retrieved successfully"
    )


@router.get("/{lob_id}", response_model=ResponseEnvelope[LineOfBusinessResponse])
async def read_line_of_business(
    *,
    lob_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[LineOfBusinessResponse]:
    """
    Get a specific line of business by id.
    """
    service = LineOfBusinessService(db)
    lob = await service.get(id=lob_id)
    if not lob:
        raise NotFoundException(message="Line of business not found")
    return ResponseEnvelope[LineOfBusinessResponse].ok(
        data=LineOfBusinessResponse.model_validate(lob),
        message="Line of business retrieved successfully",
    )


@router.patch("/{lob_id}", response_model=ResponseEnvelope[LineOfBusinessResponse])
async def update_line_of_business(
    *,
    lob_id: UUID,
    lob_in: LineOfBusinessUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[LineOfBusinessResponse]:
    """
    Update a line of business.
    """
    service = LineOfBusinessService(db)
    lob = await service.get(id=lob_id)
    if not lob:
        raise NotFoundException(message="Line of business not found")
    updated_lob = await service.update(db_obj=lob, obj_in=lob_in)
    return ResponseEnvelope[
        (
            ResponseEnvelope[LineOfBusinessResponse].ok(
                data=LineOfBusinessResponse.model_validate(updated_lob),
                message="Line of business updated successfully",
            )
            if False
            else ResponseEnvelope[LineOfBusinessResponse].ok(
                data=LineOfBusinessResponse.model_validate(updated_lob),
                message="Line of business updated successfully",
            )
        )
    ]  # Cleaned block below


@router.delete("/{lob_id}", response_model=ResponseEnvelope[LineOfBusinessResponse])
async def delete_line_of_business(
    *,
    lob_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[LineOfBusinessResponse]:
    """
    Delete a line of business.
    """
    service = LineOfBusinessService(db)
    lob = await service.get(id=lob_id)
    if not lob:
        raise NotFoundException(message="Line of business not found")
    deleted_lob = await service.remove(id=lob_id)
    return ResponseEnvelope[LineOfBusinessResponse].ok(
        data=LineOfBusinessResponse.model_validate(deleted_lob),
        message="Line of business deleted successfully",
    )
