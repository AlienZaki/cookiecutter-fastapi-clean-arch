"""
Example repository tests.

To create repository tests:
1. Create a new test file in the repositories/ directory (e.g., test_memory_repository.py)
2. Import your domain models and repository
3. Write tests for your repository methods
"""

import pytest
from app.repositories.memory_repository import MemoryRepository
from app.domain.models import Product


@pytest.mark.asyncio
async def test_repository_save() -> None:
    """Test saving a product to repository."""
    repo = MemoryRepository()
    item = Product(id="1", name="Test Product", price=10.0)
    await repo.save(item)
    items = await repo.list_all()
    assert len(items) == 1
    assert items[0].id == "1"
    assert items[0].name == "Test Product"


@pytest.mark.asyncio
async def test_repository_list_all() -> None:
    """Test listing all products from repository."""
    repo = MemoryRepository()
    item1 = Product(id="1", name="Product 1", price=10.0)
    item2 = Product(id="2", name="Product 2", price=20.0)
    await repo.save(item1)
    await repo.save(item2)
    items = await repo.list_all()
    assert len(items) == 2


@pytest.mark.asyncio
async def test_repository_list_all_with_pagination() -> None:
    """Test listing products with pagination."""
    repo = MemoryRepository()
    for i in range(5):
        await repo.save(Product(id=str(i), name=f"Product {i}", price=float(i * 10)))
    
    # Test offset
    items = await repo.list_all(offset=2)
    assert len(items) == 3
    
    # Test limit
    items = await repo.list_all(limit=2)
    assert len(items) == 2
    
    # Test offset and limit
    items = await repo.list_all(offset=1, limit=2)
    assert len(items) == 2


@pytest.mark.asyncio
async def test_repository_update() -> None:
    """Test updating a product in repository."""
    repo = MemoryRepository()
    product = Product(id="1", name="Original Name", price=10.0)
    await repo.save(product)
    
    updated_product = Product(id="1", name="Updated Name", price=20.0)
    await repo.update(updated_product)
    
    retrieved = await repo.get_product_by_id("1")
    assert retrieved is not None
    assert retrieved.name == "Updated Name"
    assert retrieved.price == 20.0


@pytest.mark.asyncio
async def test_repository_update_not_found() -> None:
    """Test updating a non-existent product raises error."""
    repo = MemoryRepository()
    product = Product(id="1", name="Test", price=10.0)
    
    with pytest.raises(ValueError, match="Product with id '1' not found"):
        await repo.update(product)


@pytest.mark.asyncio
async def test_repository_delete() -> None:
    """Test deleting a product from repository."""
    repo = MemoryRepository()
    product = Product(id="1", name="Test Product", price=10.0)
    await repo.save(product)
    
    await repo.delete("1")
    
    retrieved = await repo.get_product_by_id("1")
    assert retrieved is None


@pytest.mark.asyncio
async def test_repository_delete_not_found() -> None:
    """Test deleting a non-existent product raises error."""
    repo = MemoryRepository()
    
    with pytest.raises(ValueError, match="Product with id '1' not found"):
        await repo.delete("1")
