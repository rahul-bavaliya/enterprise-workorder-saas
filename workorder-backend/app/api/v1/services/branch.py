# app/api/v1/services/branch.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.branch import Branch
from app.api.v1.schemas.branch import BranchCreate, BranchUpdate


class BranchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[Branch]:
        return await self.db.get(Branch, id)

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[Branch]:
        result = await self.db.execute(select(Branch).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: BranchCreate) -> Branch:
        db_obj = Branch(
            business_id=obj_in.business_id,
            branch_manager_id=obj_in.branch_manager_id,
            name=obj_in.name,
            number=obj_in.number,
            lob_id=obj_in.lob_id,
            address1=obj_in.address1,
            address2=obj_in.address2,
            city=obj_in.city,
            postal_code=obj_in.postal_code,
            province=obj_in.province,
            country=obj_in.country,
            latitude=obj_in.latitude,
            longitude=obj_in.longitude,
            region=obj_in.region,
            phone=obj_in.phone,
            email=obj_in.email,
            website_url=obj_in.website_url,
            contact_person=obj_in.contact_person,
            division_name=obj_in.division_name,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: Branch, obj_in: Union[BranchUpdate, dict]
    ) -> Branch:
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

    async def remove(self, *, id: UUID) -> Optional[Branch]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
