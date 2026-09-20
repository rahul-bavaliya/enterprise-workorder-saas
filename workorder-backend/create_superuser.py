#!/usr/bin/env python3
from app.core.database import SessionLocal
from app.api.v1.services.user import UserService
from app.api.v1.schemas.user import UserCreate

def create_superuser():
    db = SessionLocal()
    user_in = UserCreate(
        email="admin@example.com",
        password="password123",
        role="admin"
    )
    user = UserService(db).create(obj_in=user_in)
    print(f"Created superuser: {user.email} with id {user.id}")

if __name__ == "__main__":
    create_superuser()