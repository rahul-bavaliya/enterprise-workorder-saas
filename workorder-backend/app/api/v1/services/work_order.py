# app/api/v1/services/work_order.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.models.work_order import (
    Asset,
    AssetCategory,
    WorkOrder,
    WorkOrderPriority,
    WorkOrderStatusLookup,
    SalesTypeLookup,
    WorkOrderTask,
)
from app.api.v1.schemas.work_order import (
    AssetCreate,
    AssetUpdate,
    AssetResponse,
    WorkOrderCreate,
    WorkOrderUpdate,
    WorkOrderResponse,
    WorkOrderTaskCreate,
    WorkOrderTaskUpdate,
    WorkOrderTaskResponse,
    WorkOrderStatusLookupCreate,
    WorkOrderStatusLookupUpdate,
    WorkOrderStatusLookupResponse,
    SalesTypeLookupCreate,
    SalesTypeLookupUpdate,
    SalesTypeLookupResponse,
)


class AssetService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[Asset]:
        return await self.db.get(Asset, id)

    async def get_by_serial(self, serial_number: str) -> Optional[Asset]:
        result = await self.db.execute(
            select(Asset).filter(Asset.serial_number == serial_number)
        )
        return result.scalars().first()

    async def get_multi_by_customer(
        self, customer_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Asset]:
        result = await self.db.execute(
            select(Asset)
            .filter(Asset.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[Asset]:
        result = await self.db.execute(select(Asset).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: AssetCreate) -> Asset:
        db_obj = Asset(
            name=obj_in.name,
            category=obj_in.category,
            serial_number=obj_in.serial_number,
            location=obj_in.location,
            customer_id=obj_in.customer_id,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, *, db_obj: Asset, obj_in: Union[AssetUpdate, dict]) -> Asset:
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

    async def remove(self, *, id: UUID) -> Optional[Asset]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj


class WorkOrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[WorkOrder]:
        return await self.db.get(WorkOrder, id)

    async def get_multi_by_customer(
        self, customer_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[WorkOrder]:
        result = await self.db.execute(
            select(WorkOrder)
            .filter(WorkOrder.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi_by_asset(
        self, asset_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[WorkOrder]:
        result = await self.db.execute(
            select(WorkOrder)
            .filter(WorkOrder.asset_id == asset_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[WorkOrder]:
        result = await self.db.execute(select(WorkOrder).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: WorkOrderCreate) -> WorkOrder:
        db_obj = WorkOrder(
            customer_id=obj_in.customer_id,
            asset_id=obj_in.asset_id,
            status_id=obj_in.status_id,
            priority=obj_in.priority,
            sales_type_id=obj_in.sales_type_id,
            assigned_technician_id=obj_in.assigned_technician_id,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: WorkOrder, obj_in: Union[WorkOrderUpdate, dict]
    ) -> WorkOrder:
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

    async def remove(self, *, id: UUID) -> Optional[WorkOrder]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj


class WorkOrderTaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[WorkOrderTask]:
        return await self.db.get(WorkOrderTask, id)

    async def get_multi_by_work_order(
        self, work_order_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[WorkOrderTask]:
        result = await self.db.execute(
            select(WorkOrderTask)
            .filter(WorkOrderTask.work_order_id == work_order_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[WorkOrderTask]:
        result = await self.db.execute(select(WorkOrderTask).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: WorkOrderTaskCreate) -> WorkOrderTask:
        db_obj = WorkOrderTask(
            title=obj_in.title,
            is_completed=obj_in.is_completed,
            work_order_id=obj_in.work_order_id,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: WorkOrderTask, obj_in: Union[WorkOrderTaskUpdate, dict]
    ) -> WorkOrderTask:
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

    async def remove(self, *, id: UUID) -> Optional[WorkOrderTask]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj


class WorkOrderStatusLookupService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[WorkOrderStatusLookup]:
        return await self.db.get(WorkOrderStatusLookup, id)

    async def get_by_name(self, name: str) -> Optional[WorkOrderStatusLookup]:
        result = await self.db.execute(
            select(WorkOrderStatusLookup).filter(WorkOrderStatusLookup.name == name)
        )
        return result.scalars().first()

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[WorkOrderStatusLookup]:
        result = await self.db.execute(
            select(WorkOrderStatusLookup).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(
        self, *, obj_in: WorkOrderStatusLookupCreate
    ) -> WorkOrderStatusLookup:
        db_obj = WorkOrderStatusLookup(
            name=obj_in.name,
            abbreviation=obj_in.abbreviation,
            description=obj_in.description,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        db_obj: WorkOrderStatusLookup,
        obj_in: Union[WorkOrderStatusLookupUpdate, dict]
    ) -> WorkOrderStatusLookup:
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

    async def remove(self, *, id: UUID) -> Optional[WorkOrderStatusLookup]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj


class SalesTypeLookupService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: UUID) -> Optional[SalesTypeLookup]:
        return await self.db.get(SalesTypeLookup, id)

    async def get_by_name(self, name: str) -> Optional[SalesTypeLookup]:
        result = await self.db.execute(
            select(SalesTypeLookup).filter(SalesTypeLookup.name == name)
        )
        return result.scalars().first()

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[SalesTypeLookup]:
        result = await self.db.execute(
            select(SalesTypeLookup).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, *, obj_in: SalesTypeLookupCreate) -> SalesTypeLookup:
        db_obj = SalesTypeLookup(
            name=obj_in.name,
            abbreviation=obj_in.abbreviation,
            description=obj_in.description,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: SalesTypeLookup, obj_in: Union[SalesTypeLookupUpdate, dict]
    ) -> SalesTypeLookup:
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

    async def remove(self, *, id: UUID) -> Optional[SalesTypeLookup]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
