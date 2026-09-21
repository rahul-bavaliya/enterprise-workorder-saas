# app/api/v1/schemas/auth.py
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str