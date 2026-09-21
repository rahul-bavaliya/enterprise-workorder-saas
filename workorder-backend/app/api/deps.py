# app/api/deps.py
from app.core.database import get_db

# Re-export get_db for cleaner imports across endpoints
__all__ = ["get_db"]
