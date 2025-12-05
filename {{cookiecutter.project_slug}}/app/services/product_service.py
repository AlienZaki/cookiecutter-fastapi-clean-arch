"""
Example service file.

To create a new service:
1. Create a new service file (e.g., product_service.py)
2. Define your service class with business logic
3. Add the service to app/core/container.py
4. Add dependency function in app/api/dependencies.py
"""

from app.domain.errors import ProductNotFoundError
from app.domain.errors import ProductValidationError
from app.domain.models import Product
from app.domain.protocols import Repository


class ProductService:
    """Service for managing products."""

    def __init__(self, repository: Repository) -> None:
        """Initialize service with repository."""
        self.repository = repository

    async def create_product(self, product: Product) -> Product:
        """Create a new product."""
        try:
            await self.repository.save(product)
            return product
        except ValueError as e:
            raise ProductValidationError(str(e)) from e

    async def get_product_by_id(self, product_id: str) -> Product:
        """Get a product by ID."""
        product = await self.repository.get_product_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    async def get_products(self, offset: int = 0, limit: int | None = None) -> list[Product]:
        """Get all products with optional pagination.
        
        Args:
            offset: Number of products to skip (for pagination)
            limit: Maximum number of products to return (None for all)
        
        Returns:
            List of products
        """
        return await self.repository.list_all(offset=offset, limit=limit)

    async def update_product(self, product: Product) -> Product:
        """Update an existing product."""
        try:
            await self.repository.update(product)
            return product
        except ValueError as e:
            raise ProductNotFoundError(str(e)) from e

    async def delete_product(self, product_id: str) -> None:
        """Delete a product by ID."""
        try:
            await self.repository.delete(product_id)
        except ValueError as e:
            raise ProductNotFoundError(str(e)) from e
