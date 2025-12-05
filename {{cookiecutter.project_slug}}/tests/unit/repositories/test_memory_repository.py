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
