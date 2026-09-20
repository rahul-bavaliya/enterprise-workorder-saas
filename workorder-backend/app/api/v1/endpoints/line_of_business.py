# app/api/v1/endpoints/line_of_business.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.line_of_business import LineOfBusinessCreate, LineOfBusinessResponse, LineOfBusinessUpdate
from app.api.v1.services.line_of_business import LineOfBusinessService

router = APIRouter()


@router.post("/", response_model=LineOfBusinessResponse, status_code=status.HTTP_201_CREATED)
def create_line_of_business(
    *,
    lob_in: LineOfBusinessCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> LineOfBusinessResponse:
    """
    Create a new line of business.
    """
    service = LineOfBusinessService(db)
    return service.create(obj_in=lob_in)


@router.get("/", response_model=List[LineOfBusinessResponse])
def read_lines_of_business(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[LineOfBusinessResponse]:
    """
    Retrieve lines of business.
    """
    service = LineOfBusinessService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{lob_id}", response_model=LineOfBusinessResponse)
def read_line_of_business(
    *,
    lob_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> LineOfBusinessResponse:
    """
    Get a specific line of business by id.
    """
    service = LineOfBusinessService(db)
    lob = service.get(id=lob_id)
    if not lob:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line of business not found",
        )
    return lob


@router.patch("/{lob_id}", response_model=LineOfBusinessResponse)
def update_line_of_business(
    *,
    lob_id: UUID,
    lob_in: LineOfBusinessUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> LineOfBusinessResponse:
    """
    Update a line of business.
    """
    service = LineOfBusinessService(db)
    lob = service.get(id=lob_id)
    if not lob:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line of business not found",
        )
    return service.update(db_obj=lob, obj_in=lob_in)


@router.delete("/{lob_id}", response_model=LineOfBusinessResponse)
def delete_line_of_business(
    *,
    lob_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> LineOfBusinessResponse:
    """
    Delete a line of business.
    """
    service = LineOfBusinessService(db)
    lob = service.get(id=lob_id)
    if not lob:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line of business not found",
        )
    return service.remove(id=lob_id)