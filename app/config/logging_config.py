"""
app/config/logging_config.py
============================
Configures application-wide logging.

- INFO and above → logs/app.log
- ERROR and above → logs/error.log
- Console output  → always on
"""

import logging
import logging.handlers
import os
from app.config.settings import settings


def setup_logging() -> None:
    """
    Call this once at application startup.
    Creates the log directory if it does not exist.
    """
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Shared formatter
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Handlers ──────────────────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(fmt)

    # Rotating file — general app log (10 MB × 5 backups)
    app_file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(settings.LOG_DIR, "app.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    app_file_handler.setLevel(log_level)
    app_file_handler.setFormatter(fmt)

    # Rotating file — errors only
    error_file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(settings.LOG_DIR, "error.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(fmt)

    # ── Root logger ───────────────────────────────────────────────────────────
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()  # Avoid duplicate handlers on reload
    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_file_handler)
    root_logger.addHandler(error_file_handler)

    logging.getLogger(__name__).info("Logging initialised. Level=%s", settings.LOG_LEVEL)
