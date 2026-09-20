# app/api/v1/services/user.py
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.user import User, UserRole
from app.core.security import get_password_hash, verify_password
from app.api.v1.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, *, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            role=obj_in.role
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        # Assuming all users are active by default; you can add an is_active column later
        return True

    def is_superuser(self, user: User) -> bool:
        return user.role == UserRole.ADMIN

    def update(
        self,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, dict]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            hashed_password = get_password_hash(update_data.pop("password"))
            update_data["hashed_password"] = hashed_password

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, *, id: UUID) -> Optional[User]:
        obj = self.db.query(User).get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj