#!/usr/bin/env python3
from app.core.database import SessionLocal
from app.api.v1.services.user import UserService
from app.api.v1.schemas.user import UserCreate

def create_superuser():
    database_session = SessionLocal()
    try:
        user_data = UserCreate(
            email="admin@example.com",
            password="password123",
            role="admin"
        )
        created_user = UserService(database_session).create(obj_in=user_data)
        print(f"Created superuser: {created_user.email} with id {created_user.id}")
    finally:
        database_session.close()

if __name__ == "__main__":
    create_superuser()