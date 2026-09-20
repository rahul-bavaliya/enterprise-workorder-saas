# app/api/v1/endpoints/sales_type.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.work_order import SalesTypeLookupCreate, SalesTypeLookupResponse, SalesTypeLookupUpdate
from app.api.v1.services.work_order import SalesTypeLookupService

router = APIRouter()


@router.post("/", response_model=SalesTypeLookupResponse, status_code=status.HTTP_201_CREATED)
def create_sales_type(
    *,
    sales_type_in: SalesTypeLookupCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> SalesTypeLookupResponse:
    """
    Create a new sales type.
    """
    service = SalesTypeLookupService(db)
    return service.create(obj_in=sales_type_in)


@router.get("/", response_model=List[SalesTypeLookupResponse])
def read_sales_types(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[SalesTypeLookupResponse]:
    """
    Retrieve sales types.
    """
    service = SalesTypeLookupService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{sales_type_id}", response_model=SalesTypeLookupResponse)
def read_sales_type(
    *,
    sales_type_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> SalesTypeLookupResponse:
    """
    Get a specific sales type by id.
    """
    service = SalesTypeLookupService(db)
    sales_type = service.get(id=sales_type_id)
    if not sales_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales type not found",
        )
    return sales_type


@router.patch("/{sales_type_id}", response_model=SalesTypeLookupResponse)
def update_sales_type(
    *,
    sales_type_id: UUID,
    sales_type_in: SalesTypeLookupUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> SalesTypeLookupResponse:
    """
    Update a sales type.
    """
    service = SalesTypeLookupService(db)
    sales_type = service.get(id=sales_type_id)
    if not sales_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales type not found",
        )
    return service.update(db_obj=sales_type, obj_in=sales_type_in)


@router.delete("/{sales_type_id}", response_model=SalesTypeLookupResponse)
def delete_sales_type(
    *,
    sales_type_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> SalesTypeLookupResponse:
    """
    Delete a sales type.
    """
    service = SalesTypeLookupService(db)
    sales_type = service.get(id=sales_type_id)
    if not sales_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales type not found",
        )
    return service.remove(id=sales_type_id)