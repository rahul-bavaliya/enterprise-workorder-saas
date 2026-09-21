# app/api/v1/endpoints/assets.py
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.asset import AssetCreate, AssetResponse, AssetUpdate
from app.api.v1.services.asset import AssetService

router = APIRouter()


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    *,
    asset_in: AssetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> AssetResponse:
    """
    Create a new asset.
    """
    service = AssetService(db)
    return service.create(obj_in=asset_in)


@router.get("/", response_model=List[AssetResponse])
def read_assets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(100, ge=1, le=100),
    customer_id: Optional[UUID] = Query(None, description="Filter by customer ID"),
    current_user = Depends(get_current_active_user)
) -> List[AssetResponse]:
    """
    Retrieve assets.
    """
    service = AssetService(db)
    if customer_id:
        return service.get_multi_by_customer(customer_id=customer_id, skip=skip, limit=limit)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{asset_id}", response_model=AssetResponse)
def read_asset(
    *,
    asset_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> AssetResponse:
    """
    Get a specific asset by id.
    """
    service = AssetService(db)
    asset = service.get(id=asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return asset


@router.patch("/{asset_id}", response_model=AssetResponse)
def update_asset(
    *,
    asset_id: UUID,
    asset_in: AssetUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> AssetResponse:
    """
    Update an asset.
    """
    service = AssetService(db)
    asset = service.get(id=asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return service.update(db_obj=asset, obj_in=asset_in)


@router.delete("/{asset_id}", response_model=AssetResponse)
def delete_asset(
    *,
    asset_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> AssetResponse:
    """
    Delete an asset.
    """
    service = AssetService(db)
    asset = service.get(id=asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return service.remove(id=asset_id)