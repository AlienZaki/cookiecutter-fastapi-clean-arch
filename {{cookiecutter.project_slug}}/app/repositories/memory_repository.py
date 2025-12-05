from app.domain.models import Product


class MemoryRepository:
    """In-memory repository for storing products."""

    def __init__(self) -> None:
        """Initialize empty storage."""
        self._items: dict[str, Product] = {}

    async def save(self, product: Product) -> None:
        """Save a product."""
        if not product.id:
            raise ValueError("Product must have an id to be saved")
        self._items[product.id] = product

    async def get_product_by_id(self, product_id: str) -> Product | None:
        """Get a product by ID."""
        return self._items.get(product_id)

    async def list_all(self, offset: int = 0, limit: int | None = None) -> list[Product]:
        """Retrieve all saved products with optional pagination."""
        products = list(self._items.values())
        if offset > 0:
            products = products[offset:]
        if limit is not None:
            products = products[:limit]
        return products

    async def update(self, product: Product) -> None:
        """Update an existing product."""
        if not product.id:
            raise ValueError("Product must have an id to be updated")
        if product.id not in self._items:
            raise ValueError(f"Product with id '{product.id}' not found")
        self._items[product.id] = product

    async def delete(self, product_id: str) -> None:
        """Delete a product by ID."""
        if product_id not in self._items:
            raise ValueError(f"Product with id '{product_id}' not found")
        del self._items[product_id]

    async def clear(self) -> None:
        """Clear all stored items (useful for testing)."""
        self._items.clear()

    def count(self) -> int:
        """Get the number of stored items."""
        return len(self._items)
