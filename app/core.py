"""Application core module. Things shared between API and CLI."""

import logging
from logging.handlers import RotatingFileHandler

from .settings import AppSettings

settings = AppSettings()

log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

handler_console = logging.StreamHandler()
handler_console.setFormatter(log_formatter)
handler_console.setLevel(settings.log_level.upper())

if settings.log_local:
    handler_file = RotatingFileHandler(
        "resources/app.log",
        maxBytes=settings.log_file_max_bytes,
        backupCount=settings.log_file_backup_count,
    )
    handler_file.setFormatter(log_formatter)
    handler_file.setLevel(settings.log_level.upper())

logging.basicConfig()
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)


def get_app_logger() -> logging.Logger:
    """Get the application logger."""
    app_logger = logging.getLogger("app")
    app_logger.setLevel(settings.log_level.upper())
    app_logger.addHandler(handler_console)
    if settings.log_local:
        app_logger.addHandler(handler_file)

    return app_logger
