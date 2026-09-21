# app/api/v1/endpoints/branch.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.branch import BranchCreate, BranchResponse, BranchUpdate
from app.api.v1.services.branch import BranchService

router = APIRouter()


@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create_branch(
    *,
    branch_in: BranchCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BranchResponse:
    """
    Create a new branch.
    """
    service = BranchService(db)
    return service.create(obj_in=branch_in)


@router.get("/", response_model=List[BranchResponse])
def read_branches(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[BranchResponse]:
    """
    Retrieve branches.
    """
    service = BranchService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{branch_id}", response_model=BranchResponse)
def read_branch(
    *,
    branch_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BranchResponse:
    """
    Get a specific branch by id.
    """
    service = BranchService(db)
    branch = service.get(id=branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found",
        )
    return branch


@router.patch("/{branch_id}", response_model=BranchResponse)
def update_branch(
    *,
    branch_id: UUID,
    branch_in: BranchUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BranchResponse:
    """
    Update a branch.
    """
    service = BranchService(db)
    branch = service.get(id=branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found",
        )
    return service.update(db_obj=branch, obj_in=branch_in)


@router.delete("/{branch_id}", response_model=BranchResponse)
def delete_branch(
    *,
    branch_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> BranchResponse:
    """
    Delete a branch.
    """
    service = BranchService(db)
    branch = service.get(id=branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found",
        )
    return service.remove(id=branch_id)