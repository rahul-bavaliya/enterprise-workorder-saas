# app/api/v1/endpoints/business.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.business import BusinessCreate, BusinessResponse, BusinessUpdate
from app.api.v1.services.business import BusinessService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[BusinessResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_business(
    *,
    business_in: BusinessCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[BusinessResponse]:
    """
    Create a new business.
    """
    service = BusinessService(db)
    business = await service.create(obj_in=business_in)
    return ResponseEnvelope[BusinessResponse].ok(
        data=BusinessResponse.model_validate(business),
        message="Business created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[BusinessResponse]])
async def read_businesses(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[BusinessResponse]]:
    """
    Retrieve businesses.
    """
    service = BusinessService(db)
    businesses = await service.get_multi(skip=skip, limit=limit)
    business_responses = [BusinessResponse.model_validate(b) for b in businesses]
    return ResponseEnvelope[List[BusinessResponse]].ok(
        data=business_responses, message="Businesses retrieved successfully"
    )


@router.get("/suggest", response_model=ResponseEnvelope[List[str]])
async def suggest_business_types(
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[str]]:
    """
    Get suggested business types.
    """
    suggestions = [
        "Restaurant",
        "Retail Store",
        "Consulting Firm",
        "Manufacturing",
        "Healthcare",
        "Education",
        "Technology",
        "Construction",
        "Financial Services",
        "Real Estate",
        "Non-profit",
        "Agriculture",
    ]
    return ResponseEnvelope[List[str]].ok(
        data=suggestions, message="Business suggestions retrieved successfully"
    )


@router.get("/{business_id}", response_model=ResponseEnvelope[BusinessResponse])
async def read_business(
    *,
    business_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[BusinessResponse]:
    """
    Get a specific business by id.
    """
    service = BusinessService(db)
    business = await service.get(id=business_id)
    if not business:
        raise NotFoundException(message="Business not found")
    return ResponseEnvelope[BusinessResponse].ok(
        data=BusinessResponse.model_validate(business),
        message="Business retrieved successfully",
    )


@router.patch("/{business_id}", response_model=ResponseEnvelope[BusinessResponse])
async def update_business(
    *,
    business_id: UUID,
    business_in: BusinessUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[BusinessResponse]:
    """
    Update a business.
    """
    service = BusinessService(db)
    business = await service.get(id=business_id)
    if not business:
        raise NotFoundException(message="Business not found")
    updated_business = await service.update(db_obj=business, obj_in=business_in)
    return ResponseEnvelope[BusinessResponse].ok(
        data=BusinessResponse.model_validate(updated_business),
        message="Business updated successfully",
    )


@router.delete("/{business_id}", response_model=ResponseEnvelope[BusinessResponse])
async def delete_business(
    *,
    business_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[BusinessResponse]:
    """
    Delete a business.
    """
    service = BusinessService(db)
    business = await service.get(id=business_id)
    if not business:
        raise NotFoundException(message="Business not found")
    deleted_business = await service.remove(id=business_id)
    return ResponseEnvelope[BusinessResponse].ok(
        data=BusinessResponse.model_validate(deleted_business),
        message="Business deleted successfully",
    )
