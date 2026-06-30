"""
app/core/response.py
=====================
Reusable API response helpers.

Using these keeps response structure consistent across all routes.

Usage:
    from app.core.response import success_response, error_response

    return success_response(data=product, message="Product created.")
    return error_response(message="Product not found.", status_code=404)
"""

from typing import Any
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> JSONResponse:
    """Return a standardised success JSON response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )


def error_response(
    message: str = "An error occurred.",
    status_code: int = 400,
    details: Any = None,
) -> JSONResponse:
    """Return a standardised error JSON response."""
    body: dict[str, Any] = {"success": False, "error": message}
    if details is not None:
        body["details"] = details
    return JSONResponse(status_code=status_code, content=body)


def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "Success",
) -> JSONResponse:
    """Return a standardised paginated list response."""
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": max(1, -(-total // page_size)),
            },
            "data": items,
        },
    )
