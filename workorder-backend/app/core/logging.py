"""app/core/logging.py"""

import logging
import sys
from pythonjsonlogger import jsonlogger  # Optional, or standard text formatting


def setup_logging():
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicate logs
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Adjust third-party loggers if needed (e.g., SQLAlchemy, Uvicorn)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.WARNING
    )  # Set to INFO if you want to see SQL queries
