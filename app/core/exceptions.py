"""
app/core/exceptions.py
=======================
Custom exception classes and global FastAPI exception handlers.

Using specific exception types makes error handling explicit and consistent
across all routes — routes just raise, handlers format the response.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


# ── Custom Exceptions ─────────────────────────────────────────────────────────

class AppException(Exception):
    """Base class for all application-specific exceptions."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: int | str) -> None:
        super().__init__(
            message=f"{resource} with id={resource_id!r} was not found.",
            status_code=404,
        )


class ValidationException(AppException):
    """Raised when input data fails business-level validation."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=422)


class ScrapingException(AppException):
    """Raised when a scraping job fails."""

    def __init__(self, url: str, reason: str) -> None:
        super().__init__(
            message=f"Scraping failed for URL={url!r}. Reason: {reason}",
            status_code=500,
        )


# ── Exception Handlers ────────────────────────────────────────────────────────

def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.error("AppException [%d]: %s", exc.status_code, exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "An unexpected server error occurred."},
        )
