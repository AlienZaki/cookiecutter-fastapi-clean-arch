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

    async def get_products(self) -> list[Product]:
        """Get all products."""
        return await self.repository.list_all()
