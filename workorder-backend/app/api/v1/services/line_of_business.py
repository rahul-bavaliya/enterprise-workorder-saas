# app/api/v1/services/line_of_business.py
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models.line_of_business import LineOfBusiness
from app.api.v1.schemas.line_of_business import LineOfBusinessCreate, LineOfBusinessUpdate, LineOfBusinessResponse


class LineOfBusinessService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[LineOfBusiness]:
        return self.db.query(LineOfBusiness).filter(LineOfBusiness.id == id).first()

    def get_by_name(self, name: str) -> Optional[LineOfBusiness]:
        return self.db.query(LineOfBusiness).filter(LineOfBusiness.lob_name == name).first()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[LineOfBusiness]:
        return self.db.query(LineOfBusiness).offset(skip).limit(limit).all()

    def create(self, *, obj_in: LineOfBusinessCreate) -> LineOfBusiness:
        db_obj = LineOfBusiness(
            division_name=obj_in.division_name,
            division_abbreviation=obj_in.division_abbreviation,
            lob_name=obj_in.lob_name,
            is_active=obj_in.is_active
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: LineOfBusiness,
        obj_in: LineOfBusinessUpdate
    ) -> LineOfBusiness:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, *, id: UUID) -> Optional[LineOfBusiness]:
        obj = self.db.query(LineOfBusiness).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj