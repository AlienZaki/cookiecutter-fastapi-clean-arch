"""
Domain-specific exceptions.

This module contains pure domain exceptions with no framework dependencies.
To handle these exceptions in FastAPI, 
create and register error handlers in app/api/error_handlers.py
"""


class ProductNotFoundError(Exception):
    """Raised when a product is not found."""

    def __init__(self, product_id: str) -> None:
        self.product_id = product_id
        super().__init__(f"Product '{product_id}' not found")


class ProductValidationError(Exception):
    """Raised when product validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
