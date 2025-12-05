"""
Example service tests.

To create service tests:
1. Create a new test file in the services/ directory (e.g., test_product_service.py)
2. Import your service and domain models
3. Write tests for your service methods
"""

import pytest
from app.domain.models import Product
from app.repositories.memory_repository import MemoryRepository
from app.services.product_service import ProductService


@pytest.mark.asyncio
async def test_product_service_create() -> None:
    """Test creating a product through service."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    product = Product(id="1", name="Test Product", price=10.0)
    created = await service.create_product(product)
    assert created.id == "1"
    assert created.name == "Test Product"


@pytest.mark.asyncio
async def test_product_service_get_products() -> None:
    """Test getting all products through service."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    product1 = Product(id="1", name="Product 1", price=10.0)
    product2 = Product(id="2", name="Product 2", price=20.0)
    await service.create_product(product1)
    await service.create_product(product2)
    products = await service.get_products()
    assert len(products) == 2
