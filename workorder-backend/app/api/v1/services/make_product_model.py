# app/api/v1/services/make_product_model.py
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models.make_product_model import MakeProductModel
from app.api.v1.schemas.make_product_model import (
    MakeProductModelCreate,
    MakeProductModelUpdate,
    MakeProductModelResponse,
)


class MakeProductModelService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[MakeProductModel]:
        return self.db.query(MakeProductModel).filter(MakeProductModel.id == id).first()

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[MakeProductModel]:
        return self.db.query(MakeProductModel).offset(skip).limit(limit).all()

    def create(self, *, obj_in: MakeProductModelCreate) -> MakeProductModel:
        db_obj = MakeProductModel(
            product_id=obj_in.product_id,
            model_id=obj_in.model_id,
            category_id=obj_in.category_id,
            sub_category_id=obj_in.sub_category_id,
            make=obj_in.make,
            model=obj_in.model,
            decal_model=obj_in.decal_model,
            category=obj_in.category,
            sub_category=obj_in.sub_category,
            division=obj_in.division,
            jd_product_family=obj_in.jd_product_family,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: MakeProductModel, obj_in: MakeProductModelUpdate
    ) -> MakeProductModel:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, *, id: UUID) -> Optional[MakeProductModel]:
        obj = self.db.query(MakeProductModel).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
