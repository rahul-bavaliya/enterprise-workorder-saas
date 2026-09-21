# app/api/v1/endpoints/customers.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.api.v1.services.customer import CustomerService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[CustomerResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    *,
    customer_in: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[CustomerResponse]:
    """
    Create a new customer.
    """
    service = CustomerService(db)
    customer = await service.create(obj_in=customer_in)
    return ResponseEnvelope[CustomerResponse].ok(
        data=CustomerResponse.model_validate(customer),
        message="Customer created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[CustomerResponse]])
async def read_customers(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
) -> ResponseEnvelope[List[CustomerResponse]]:
    """
    Retrieve customers.
    """
    service = CustomerService(db)
    customers = await service.get_multi(skip=skip, limit=limit)
    customer_responses = [CustomerResponse.model_validate(c) for c in customers]
    return ResponseEnvelope[List[CustomerResponse]].ok(
        data=customer_responses, message="Customers retrieved successfully"
    )


@router.get("/{customer_id}", response_model=ResponseEnvelope[CustomerResponse])
async def read_customer(
    *,
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[CustomerResponse]:
    """
    Get customer by ID.
    """
    service = CustomerService(db)
    customer = await service.get(id=customer_id)
    if not customer:
        raise NotFoundException(message="Customer not found")
    return ResponseEnvelope[CustomerResponse].ok(
        data=CustomerResponse.model_validate(customer),
        message="Customer retrieved successfully",
    )


@router.patch("/{customer_id}", response_model=ResponseEnvelope[CustomerResponse])
async def update_customer(
    *,
    customer_id: UUID,
    customer_in: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[CustomerResponse]:
    """
    Update a customer.
    """
    service = CustomerService(db)
    customer = await service.get(id=customer_id)
    if not customer:
        raise NotFoundException(message="Customer not found")
    updated_customer = await service.update(db_obj=customer, obj_in=customer_in)
    return ResponseEnvelope[CustomerResponse].ok(
        data=CustomerResponse.model_validate(updated_customer),
        message="Customer updated successfully",
    )


@router.delete("/{customer_id}", response_model=ResponseEnvelope[CustomerResponse])
async def delete_customer(
    *,
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
) -> ResponseEnvelope[CustomerResponse]:
    """
    Delete a customer.
    """
    service = CustomerService(db)
    customer = await service.get(id=customer_id)
    if not customer:
        raise NotFoundException(message="Customer not found")
    deleted_customer = await service.remove(id=customer_id)
    return ResponseEnvelope[CustomerResponse].ok(
        data=CustomerResponse.model_validate(deleted_customer),
        message="Customer deleted successfully",
    )
