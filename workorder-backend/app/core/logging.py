"""app/core/logging.py"""

import logging
import sys
try:
    from pythonjsonlogger import jsonlogger  # Optional, or standard text formatting
    HAS_JSON_LOGGER = True
except ImportError:
    jsonlogger = None
    HAS_JSON_LOGGER = False


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels."""

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logging():
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicate logs
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Console handler with colored formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter())
    root_logger.addHandler(handler)

    # Adjust third-party loggers if needed (e.g., SQLAlchemy, Uvicorn)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.WARNING
    )  # Set to INFO if you want to see SQL queries