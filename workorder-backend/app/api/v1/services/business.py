# app/api/v1/services/business.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.business import Business
from app.api.v1.schemas.business import BusinessCreate, BusinessUpdate


class BusinessService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[Business]:
        return await self.db.get(Business, id)

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[Business]:
        result = await self.db.execute(select(Business).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: BusinessCreate) -> Business:
        db_obj = Business(
            name=obj_in.name,
            description=obj_in.description,
            email=obj_in.email,
            phone=obj_in.phone,
            address1=obj_in.address1,
            address2=obj_in.address2,
            city=obj_in.city,
            state=obj_in.state,
            country=obj_in.country,
            postal_code=obj_in.postal_code,
            website_url=obj_in.website_url,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: Business, obj_in: Union[BusinessUpdate, dict]
    ) -> Business:
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

    async def remove(self, *, id: UUID) -> Optional[Business]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
