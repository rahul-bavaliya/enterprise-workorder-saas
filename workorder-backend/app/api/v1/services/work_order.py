# app/api/v1/services/work_order.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

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
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == id).first()

    def get_by_serial(self, serial_number: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.serial_number == serial_number).first()

    def get_multi_by_customer(
        self, customer_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Asset]:
        return (
            self.db.query(Asset)
            .filter(Asset.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[Asset]:
        return self.db.query(Asset).offset(skip).limit(limit).all()

    def create(self, *, obj_in: AssetCreate) -> Asset:
        db_obj = Asset(
            name=obj_in.name,
            category=obj_in.category,
            serial_number=obj_in.serial_number,
            location=obj_in.location,
            customer_id=obj_in.customer_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: Asset,
        obj_in: Union[AssetUpdate, dict]
    ) -> Asset:
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

    def remove(self, *, id: UUID) -> Optional[Asset]:
        obj = self.db.query(Asset).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj


class WorkOrderService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[WorkOrder]:
        return (
            self.db.query(WorkOrder)
            .filter(WorkOrder.id == id)
            .first()
        )

    def get_multi_by_customer(
        self, customer_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[WorkOrder]:
        return (
            self.db.query(WorkOrder)
            .filter(WorkOrder.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_asset(
        self, asset_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[WorkOrder]:
        return (
            self.db.query(WorkOrder)
            .filter(WorkOrder.asset_id == asset_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[WorkOrder]:
        return self.db.query(WorkOrder).offset(skip).limit(limit).all()

    def create(self, *, obj_in: WorkOrderCreate) -> WorkOrder:
        db_obj = WorkOrder(
            customer_id=obj_in.customer_id,
            asset_id=obj_in.asset_id,
            status_id=obj_in.status_id,
            priority=obj_in.priority,
            sales_type_id=obj_in.sales_type_id,
            assigned_technician_id=obj_in.assigned_technician_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: WorkOrder,
        obj_in: Union[WorkOrderUpdate, dict]
    ) -> WorkOrder:
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

    def remove(self, *, id: UUID) -> Optional[WorkOrder]:
        obj = self.db.query(WorkOrder).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj


class WorkOrderTaskService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[WorkOrderTask]:
        return (
            self.db.query(WorkOrderTask)
            .filter(WorkOrderTask.id == id)
            .first()
        )

    def get_multi_by_work_order(
        self, work_order_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[WorkOrderTask]:
        return (
            self.db.query(WorkOrderTask)
            .filter(WorkOrderTask.work_order_id == work_order_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, *, obj_in: WorkOrderTaskCreate) -> WorkOrderTask:
        db_obj = WorkOrderTask(
            title=obj_in.title,
            is_completed=obj_in.is_completed,
            work_order_id=obj_in.work_order_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: WorkOrderTask,
        obj_in: Union[WorkOrderTaskUpdate, dict]
    ) -> WorkOrderTask:
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

    def remove(self, *, id: UUID) -> Optional[WorkOrderTask]:
        obj = self.db.query(WorkOrderTask).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj


class WorkOrderStatusLookupService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[WorkOrderStatusLookup]:
        return (
            self.db.query(WorkOrderStatusLookup)
            .filter(WorkOrderStatusLookup.id == id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[WorkOrderStatusLookup]:
        return (
            self.db.query(WorkOrderStatusLookup)
            .filter(WorkOrderStatusLookup.name == name)
            .first()
        )

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[WorkOrderStatusLookup]:
        return self.db.query(WorkOrderStatusLookup).offset(skip).limit(limit).all()

    def create(self, *, obj_in: WorkOrderStatusLookupCreate) -> WorkOrderStatusLookup:
        db_obj = WorkOrderStatusLookup(
            name=obj_in.name,
            abbreviation=obj_in.abbreviation,
            description=obj_in.description,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
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
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, *, id: UUID) -> Optional[WorkOrderStatusLookup]:
        obj = self.db.query(WorkOrderStatusLookup).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj


class SalesTypeLookupService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[SalesTypeLookup]:
        return (
            self.db.query(SalesTypeLookup)
            .filter(SalesTypeLookup.id == id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[SalesTypeLookup]:
        return (
            self.db.query(SalesTypeLookup)
            .filter(SalesTypeLookup.name == name)
            .first()
        )

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[SalesTypeLookup]:
        return self.db.query(SalesTypeLookup).offset(skip).limit(limit).all()

    def create(self, *, obj_in: SalesTypeLookupCreate) -> SalesTypeLookup:
        db_obj = SalesTypeLookup(
            name=obj_in.name,
            abbreviation=obj_in.abbreviation,
            description=obj_in.description,
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: SalesTypeLookup,
        obj_in: Union[SalesTypeLookupUpdate, dict]
    ) -> SalesTypeLookup:
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

    def remove(self, *, id: UUID) -> Optional[SalesTypeLookup]:
        obj = self.db.query(SalesTypeLookup).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj