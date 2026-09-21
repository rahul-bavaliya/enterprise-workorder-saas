# app/api/v1/services/asset.py
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models.work_order import Asset
from app.api.v1.schemas.asset import AssetCreate, AssetUpdate, AssetResponse


class AssetService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == id).first()

    def get_by_customer(self, customer_id: UUID) -> List[Asset]:
        return self.db.query(Asset).filter(Asset.customer_id == customer_id).all()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[Asset]:
        return self.db.query(Asset).offset(skip).limit(limit).all()

    def get_multi_by_customer(
        self, *, customer_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Asset]:
        return (
            self.db.query(Asset)
            .filter(Asset.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, *, obj_in: AssetCreate) -> Asset:
        db_obj = Asset(
            customer_id=obj_in.customer_id,
            name=obj_in.name,
            category=obj_in.category,
            serial_number=obj_in.serial_number,
            location=obj_in.location
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: Asset,
        obj_in: AssetUpdate
    ) -> Asset:
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