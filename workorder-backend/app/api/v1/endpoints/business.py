# app/api/v1/endpoints/business.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.business import BusinessCreate, BusinessResponse, BusinessUpdate
from app.api.v1.services.business import BusinessService

router = APIRouter()


@router.post("/", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
def create_business(
    *,
    business_in: BusinessCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BusinessResponse:
    """
    Create a new business.
    """
    service = BusinessService(db)
    return service.create(obj_in=business_in)


@router.get("/", response_model=List[BusinessResponse])
def read_businesses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[BusinessResponse]:
    """
    Retrieve businesses.
    """
    service = BusinessService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/suggest", response_model=List[str])
def suggest_business_types(
    current_user = Depends(get_current_active_user)
) -> List[str]:
    """
    Get suggested business types.
    """
    return [
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
        "Agriculture"
    ]


@router.get("/{business_id}", response_model=BusinessResponse)
def read_business(
    *,
    business_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BusinessResponse:
    """
    Get a specific business by id.
    """
    service = BusinessService(db)
    business = service.get(id=business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found",
        )
    return business


@router.patch("/{business_id}", response_model=BusinessResponse)
def update_business(
    *,
    business_id: UUID,
    business_in: BusinessUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BusinessResponse:
    """
    Update a business.
    """
    service = BusinessService(db)
    business = service.get(id=business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found",
        )
    return service.update(db_obj=business, obj_in=business_in)


@router.delete("/{business_id}", response_model=BusinessResponse)
def delete_business(
    *,
    business_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BusinessResponse:
    """
    Delete a business.
    """
    service = BusinessService(db)
    business = service.get(id=business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found",
        )
    return service.remove(id=business_id)