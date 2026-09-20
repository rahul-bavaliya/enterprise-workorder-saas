"""app/core/database.py"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL, echo=settings.SQL_ECHO, future=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db() -> Session:
    logger.info("Creating database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
