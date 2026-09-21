# app/api/v1/endpoints/make_product_model.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.make_product_model import MakeProductModelCreate, MakeProductModelResponse, MakeProductModelUpdate
from app.api.v1.services.make_product_model import MakeProductModelService

router = APIRouter()


@router.post("/", response_model=MakeProductModelResponse, status_code=status.HTTP_201_CREATED)
def create_make_product_model(
    *,
    model_in: MakeProductModelCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> MakeProductModelResponse:
    """
    Create a new make product model.
    """
    service = MakeProductModelService(db)
    return service.create(obj_in=model_in)


@router.get("/", response_model=List[MakeProductModelResponse])
def read_make_product_models(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[MakeProductModelResponse]:
    """
    Retrieve make product models.
    """
    service = MakeProductModelService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{model_id}", response_model=MakeProductModelResponse)
def read_make_product_model(
    *,
    model_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> MakeProductModelResponse:
    """
    Get a specific make product model by id.
    """
    service = MakeProductModelService(db)
    model = service.get(id=model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Make product model not found",
        )
    return model


@router.patch("/{model_id}", response_model=MakeProductModelResponse)
def update_make_product_model(
    *,
    model_id: UUID,
    model_in: MakeProductModelUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> MakeProductModelResponse:
    """
    Update a make product model.
    """
    service = MakeProductModelService(db)
    model = service.get(id=model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Make product model not found",
        )
    return service.update(db_obj=model, obj_in=model_in)


@router.delete("/{model_id}", response_model=MakeProductModelResponse)
def delete_make_product_model(
    *,
    model_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> MakeProductModelResponse:
    """
    Delete a make product model.
    """
    service = MakeProductModelService(db)
    model = service.get(id=model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Make product model not found",
        )
    return service.remove(id=model_id)