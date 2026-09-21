# app/api/v1/endpoints/users.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.v1.services.user import UserService


router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Create a new user.
    """
    service = UserService(db)
    return service.create(obj_in=user_in)


@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[UserResponse]:
    """
    Retrieve users.
    """
    service = UserService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    *,
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> UserResponse:
    """
    Get a specific user by id.
    """
    service = UserService(db)
    user = service.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    user_id: UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> UserResponse:
    """
    Update a user.
    """
    service = UserService(db)
    user = service.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return service.update(db_obj=user, obj_in=user_in)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    *,
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> UserResponse:
    """
    Delete a user.
    """
    service = UserService(db)
    user = service.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return service.remove(id=user_id)