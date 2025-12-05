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

    async def list_all(self) -> list[Product]:
        """Retrieve all saved products."""
        return list(self._items.values())

    async def clear(self) -> None:
        """Clear all stored items (useful for testing)."""
        self._items.clear()

    def count(self) -> int:
        """Get the number of stored items."""
        return len(self._items)
