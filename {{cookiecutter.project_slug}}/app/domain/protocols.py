"""
Example protocol file.

To create a new protocol:
1. Import Protocol from typing
2. Define your protocol interface
3. Import it in app/core/container.py and app/api/dependencies.py
"""

from typing import Protocol

from app.domain.models import Product


class Repository(Protocol):
    """Protocol for product persistence."""

    async def save(self, product: Product) -> None:
        """Save a product."""
        ...

    async def get_product_by_id(self, product_id: str) -> Product | None:
        """Get a product by ID."""
        ...

    async def list_all(self) -> list[Product]:
        """Retrieve all products."""
        ...
