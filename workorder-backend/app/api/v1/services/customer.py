# app/api/v1/services/customer.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.models.customer import Customer
from app.api.v1.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[Customer]:
        return await self.db.get(Customer, id)

    async def get_by_email(self, email: str) -> Optional[Customer]:
        result = await self.db.execute(select(Customer).filter(Customer.email == email))
        return result.scalars().first()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[Customer]:
        result = await self.db.execute(select(Customer).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: CustomerCreate) -> Customer:
        db_obj = Customer(
            name=obj_in.name,
            email=obj_in.email,
            phone=obj_in.phone,
            address=obj_in.address,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: Customer, obj_in: Union[CustomerUpdate, dict]
    ) -> Customer:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, *, id: UUID) -> Optional[Customer]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Customer))
        return result.scalar_one()
