"""
Example service tests.

To create service tests:
1. Create a new test file in the services/ directory (e.g., test_product_service.py)
2. Import your service and domain models
3. Write tests for your service methods
"""

import pytest

from app.domain.errors import ProductNotFoundError
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


@pytest.mark.asyncio
async def test_product_service_get_product_by_id_not_found() -> None:
    """Test getting a product by ID when product does not exist."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    with pytest.raises(ProductNotFoundError, match="Product 'non-existent' not found"):
        await service.get_product_by_id("non-existent")


@pytest.mark.asyncio
async def test_product_service_get_products_with_pagination() -> None:
    """Test getting products with pagination."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    for i in range(5):
        product = Product(id=str(i), name=f"Product {i}", price=float(i * 10))
        await service.create_product(product)
    
    # Test offset
    products = await service.get_products(offset=2)
    assert len(products) == 3
    
    # Test limit
    products = await service.get_products(limit=2)
    assert len(products) == 2
    
    # Test offset and limit
    products = await service.get_products(offset=1, limit=2)
    assert len(products) == 2


@pytest.mark.asyncio
async def test_product_service_update_product() -> None:
    """Test updating a product through service."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    product = Product(id="1", name="Original Name", price=10.0)
    await service.create_product(product)
    
    updated_product = Product(id="1", name="Updated Name", price=20.0)
    updated = await service.update_product(updated_product)
    
    assert updated.name == "Updated Name"
    assert updated.price == 20.0
    
    # Verify it's actually updated in repository
    retrieved = await service.get_product_by_id("1")
    assert retrieved.name == "Updated Name"


@pytest.mark.asyncio
async def test_product_service_update_product_not_found() -> None:
    """Test updating a non-existent product raises error."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    product = Product(id="1", name="Test", price=10.0)
    
    with pytest.raises(ProductNotFoundError):
        await service.update_product(product)


@pytest.mark.asyncio
async def test_product_service_delete_product() -> None:
    """Test deleting a product through service."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    product = Product(id="1", name="Test Product", price=10.0)
    await service.create_product(product)
    
    await service.delete_product("1")
    
    # Verify it's deleted
    with pytest.raises(ProductNotFoundError):
        await service.get_product_by_id("1")


@pytest.mark.asyncio
async def test_product_service_delete_product_not_found() -> None:
    """Test deleting a non-existent product raises error."""
    repo = MemoryRepository()
    service = ProductService(repository=repo)
    
    with pytest.raises(ProductNotFoundError):
        await service.delete_product("non-existent")
