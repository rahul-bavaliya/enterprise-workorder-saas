# app/api/v1/endpoints/users.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.user import (
    UserCreate,
    UserDeleteResponse,
    UserResponse,
    UserUpdate,
)
from app.api.v1.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=ResponseEnvelope[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    *,
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseEnvelope[UserResponse]:
    """
    Create a new user.
    """
    service = UserService(db)
    user = await service.create(obj_in=user_in)

    return ResponseEnvelope[UserResponse].ok(
        data=UserResponse.model_validate(user),
        message="User created successfully",
    )


@router.get(
    "/",
    response_model=ResponseEnvelope[List[UserResponse]],
)
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[UserResponse]]:
    """
    Retrieve users.
    """
    service = UserService(db)
    users = await service.get_multi(skip=skip, limit=limit)

    user_responses = [UserResponse.model_validate(user) for user in users]

    return ResponseEnvelope[List[UserResponse]].ok(
        data=user_responses,
        message="Users retrieved successfully",
    )


@router.get(
    "/{user_id}",
    response_model=ResponseEnvelope[UserResponse],
)
async def read_user(
    *,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[UserResponse]:
    """
    Get a specific user by ID.
    """
    service = UserService(db)
    user = await service.get(id=user_id)

    if not user:
        raise NotFoundException(message="User not found")

    return ResponseEnvelope[UserResponse].ok(
        data=UserResponse.model_validate(user),
        message="User retrieved successfully",
    )


@router.patch(
    "/{user_id}",
    response_model=ResponseEnvelope[UserResponse],
)
async def update_user(
    *,
    user_id: UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[UserResponse]:
    """
    Update a user.
    """
    service = UserService(db)
    user = await service.get(id=user_id)

    if not user:
        raise NotFoundException(message="User not found")

    updated_user = await service.update(db_obj=user, obj_in=user_in)

    return ResponseEnvelope[UserResponse].ok(
        data=UserResponse.model_validate(updated_user),
        message="User updated successfully",
    )


@router.delete(
    "/{user_id}",
    response_model=ResponseEnvelope[UserDeleteResponse],
)
async def delete_user(
    *,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[UserDeleteResponse]:
    """
    Delete a user.
    """
    service = UserService(db)
    user = await service.get(id=user_id)

    if not user:
        raise NotFoundException(message="User not found")

    deleted_user = UserDeleteResponse(
        email=user.email,
        role=user.role,
    )

    await service.remove(id=user_id)

    return ResponseEnvelope[UserDeleteResponse].ok(
        data=deleted_user,
        message="User deleted successfully",
    )
