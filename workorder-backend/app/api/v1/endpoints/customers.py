# app/api/v1/endpoints/customers.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.api.v1.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.api.v1.services.customer import CustomerService

router = APIRouter()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    *,
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> CustomerResponse:
    """
    Create a new customer.
    """
    service = CustomerService(db)
    return service.create(obj_in=customer_in)


@router.get("/", response_model=List[CustomerResponse])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
) -> List[CustomerResponse]:
    """
    Retrieve customers.
    """
    service = CustomerService(db)
    return service.get_multi(skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(
    *,
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> CustomerResponse:
    """
    Get customer by ID.
    """
    service = CustomerService(db)
    customer = service.get(id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    *,
    customer_id: UUID,
    customer_in: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> CustomerResponse:
    """
    Update a customer = customer_repository.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    customer = customer_repository.update(db=db, db_obj=customer, obj_in=customer_in)
    return customer
    """
    service = CustomerService(db)
    customer = service.get(id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return service.update(db_obj=customer, obj_in=customer_in)


@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(
    *,
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> CustomerResponse:
    """
    Delete a customer.
    """
    service = CustomerService(db)
    customer = service.get(id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return service.remove(id=customer_id)