# app/api/v1/services/department.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.department import Department
from app.api.v1.schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[Department]:
        return await self.db.get(Department, id)

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[Department]:
        result = await self.db.execute(select(Department).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: DepartmentCreate) -> Department:
        db_obj = Department(
            name=obj_in.name,
            description=obj_in.description,
            branch_id=obj_in.branch_id,
            manager_id=obj_in.manager_id,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: Department, obj_in: Union[DepartmentUpdate, dict]
    ) -> Department:
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

    async def remove(self, *, id: UUID) -> Optional[Department]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
