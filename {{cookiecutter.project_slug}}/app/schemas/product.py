"""
Example schema file.

To create a new schema:
1. Create a new schema file (e.g., product.py)
2. Define your request/response schemas using Pydantic BaseModel
"""

from pydantic import BaseModel

from app.domain.models import Product


class ProductSchema(BaseModel):
    """API schema for product data."""

    id: str
    name: str
    price: float
    in_stock: bool = True

    @classmethod
    def from_domain(cls, product: Product) -> "ProductSchema":
        """Create schema from domain model."""
        return cls(
            id=product.id,
            name=product.name,
            price=product.price,
            in_stock=product.in_stock,
        )


class ProductCreateRequest(BaseModel):
    """Request schema for creating a product."""

    name: str
    price: float
    in_stock: bool = True


class ProductsListResponse(BaseModel):
    """Response schema for product list."""

    products: list[ProductSchema]
    count: int

