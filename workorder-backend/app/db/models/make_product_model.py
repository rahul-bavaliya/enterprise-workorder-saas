# app/db/models/make_product_model.py
import uuid
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class MakeProductModel(Base):
    __tablename__ = "make_product_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(Integer, nullable=False)
    model_id = Column(Integer, nullable=True)
    category_id = Column(Integer, nullable=True)
    sub_category_id = Column(Integer, nullable=True)
    make = Column(String(255), nullable=False)
    model = Column(String(500), nullable=False)
    decal_model = Column(String(500), nullable=True)
    category = Column(String(255), nullable=False)
    sub_category = Column(String(255), nullable=True)
    division = Column(String(100), nullable=True)
    jd_product_family = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())