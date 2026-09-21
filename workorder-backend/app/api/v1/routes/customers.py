"""
Customer API routes.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.db.repository.customer import customer_repository
from app.core.dependencies import get_db, get_current_active_user

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
    customer = customer_repository.create(db=db, obj_in=customer_in)
    return customer


@router.get("/", response_model=List[CustomerResponse])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_active_user)
) -> List[CustomerResponse]:
    """
    Retrieve customers.
    """
    customers = customer_repository.get_multi(db=db, skip=skip, limit=limit)
    return customers


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
    customer = customer_repository.get(db=db, id=customer_id)
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
    Update a customer.
    """
    customer = customer_repository.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    customer = customer_repository.update(db=db, db_obj=customer, obj_in=customer_in)
    return customer


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
    customer = customer_repository.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    customer = customer_repository.remove(db=db, id=customer_id)
    return customer