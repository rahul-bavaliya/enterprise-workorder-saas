# app/api/v1/services/line_of_business.py
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.line_of_business import LineOfBusiness
from app.api.v1.schemas.line_of_business import (
    LineOfBusinessCreate,
    LineOfBusinessUpdate,
)


class LineOfBusinessService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[LineOfBusiness]:
        return await self.db.get(LineOfBusiness, id)

    async def get_by_name(self, name: str) -> Optional[LineOfBusiness]:
        result = await self.db.execute(
            select(LineOfBusiness).filter(LineOfBusiness.lob_name == name)
        )
        return result.scalars().first()

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[LineOfBusiness]:
        result = await self.db.execute(select(LineOfBusiness).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: LineOfBusinessCreate) -> LineOfBusiness:
        db_obj = LineOfBusiness(
            division_name=obj_in.division_name,
            division_abbreviation=obj_in.division_abbreviation,
            lob_name=obj_in.lob_name,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: LineOfBusiness, obj_in: LineOfBusinessUpdate
    ) -> LineOfBusiness:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, *, id: UUID) -> Optional[LineOfBusiness]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
