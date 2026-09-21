# app/api/v1/services/business.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.business import Business
from app.api.v1.schemas.business import BusinessCreate, BusinessUpdate


class BusinessService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[Business]:
        return self.db.query(Business).filter(Business.id == id).first()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[Business]:
        return self.db.query(Business).offset(skip).limit(limit).all()

    def create(self, *, obj_in: BusinessCreate) -> Business:
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
            is_active=obj_in.is_active
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: Business,
        obj_in: Union[BusinessUpdate, dict]
    ) -> Business:
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

    def remove(self, *, id: UUID) -> Optional[Business]:
        obj = self.db.query(Business).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj