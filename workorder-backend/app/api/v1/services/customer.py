# app/api/v1/services/customer.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.models.customer import Customer
from app.api.v1.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == id).first()

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.email == email).first()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[Customer]:
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def create(self, *, obj_in: CustomerCreate) -> Customer:
        db_obj = Customer(
            name=obj_in.name,
            email=obj_in.email,
            phone=obj_in.phone,
            address=obj_in.address
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: Customer,
        obj_in: Union[CustomerUpdate, dict]
    ) -> Customer:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, *, id: UUID) -> Optional[Customer]:
        obj = self.db.query(Customer).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    def count(self) -> int:
        return self.db.query(Customer).count()