# app/api/v1/services/branch.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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

    async def create(self, *, obj_in: BranchCreate) -> Optional[Branch]:
        data = obj_in.model_dump()

        db_obj = Branch(**data)
        self.db.add(db_obj)

        try:
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            # Rollback the failed transaction so the session remains usable for next rows
            await self.db.rollback()
            # Depending on your use case, you can either return None,
            # re-raise a custom HTTPException, or handle upsert logic here.
            return None

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
