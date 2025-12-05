"""
FastAPI error handlers for domain exceptions.

To customize error handling:
1. Add your custom error handlers here
2. Register them in app/api/router.py
"""

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from app.domain.errors import EntityNotFoundError
from app.domain.errors import EntityValidationError


async def entity_not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle EntityNotFoundError exceptions."""
    if not isinstance(exc, EntityNotFoundError):
        raise TypeError("Expected EntityNotFoundError")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": str(exc), "entity_id": exc.entity_id},
    )


async def entity_validation_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle EntityValidationError exceptions."""
    if not isinstance(exc, EntityValidationError):
        raise TypeError("Expected EntityValidationError")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": str(exc)},
    )

