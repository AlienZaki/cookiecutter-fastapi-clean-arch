"""
FastAPI error handlers for domain exceptions.

To customize error handling:
1. Add your custom error handlers here
2. Register them in app/api/router.py
"""

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from app.domain.errors import ProductNotFoundError
from app.domain.errors import ProductValidationError


async def product_not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle ProductNotFoundError exceptions."""
    if not isinstance(exc, ProductNotFoundError):
        raise TypeError("Expected ProductNotFoundError")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": str(exc), "product_id": exc.product_id},
    )


async def product_validation_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle ProductValidationError exceptions."""
    if not isinstance(exc, ProductValidationError):
        raise TypeError("Expected ProductValidationError")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": str(exc)},
    )

