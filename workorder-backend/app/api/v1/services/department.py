# app/api/v1/services/department.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.department import Department
from app.api.v1.schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[Department]:
        return self.db.query(Department).filter(Department.id == id).first()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[Department]:
        return self.db.query(Department).offset(skip).limit(limit).all()

    def create(self, *, obj_in: DepartmentCreate) -> Department:
        db_obj = Department(
            name=obj_in.name,
            description=obj_in.description,
            branch_id=obj_in.branch_id,
            manager_id=obj_in.manager_id,
            is_active=obj_in.is_active
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: Department,
        obj_in: Union[DepartmentUpdate, dict]
    ) -> Department:
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

    def remove(self, *, id: UUID) -> Optional[Department]:
        obj = self.db.query(Department).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj