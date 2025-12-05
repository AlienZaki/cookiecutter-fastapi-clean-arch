"""
Example repository tests.

To create repository tests:
1. Create a new test file in the repositories/ directory (e.g., test_memory_repository.py)
2. Import your domain models and repository
3. Write tests for your repository methods
"""

import pytest

from app.domain.models import Entity
from app.repositories.memory_repository import MemoryRepository


@pytest.mark.asyncio
async def test_repository_save() -> None:
    """Test saving an entity to repository."""
    repo = MemoryRepository()
    item = Entity(id="1", name="Test Entity", price=10.0)
    await repo.save(item)
    items = await repo.list_all()
    assert len(items) == 1
    assert items[0].id == "1"
    assert items[0].name == "Test Entity"


@pytest.mark.asyncio
async def test_repository_list_all() -> None:
    """Test listing all entities from repository."""
    repo = MemoryRepository()
    item1 = Entity(id="1", name="Entity 1", price=10.0)
    item2 = Entity(id="2", name="Entity 2", price=20.0)
    await repo.save(item1)
    await repo.save(item2)
    items = await repo.list_all()
    assert len(items) == 2


@pytest.mark.asyncio
async def test_repository_list_all_with_pagination() -> None:
    """Test listing entities with pagination."""
    repo = MemoryRepository()
    for i in range(5):
        await repo.save(Entity(id=str(i), name=f"Entity {i}", price=float(i * 10)))

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
    """Test updating an entity in repository."""
    repo = MemoryRepository()
    entity = Entity(id="1", name="Original Name", price=10.0)
    await repo.save(entity)

    updated_entity = Entity(id="1", name="Updated Name", price=20.0)
    await repo.update(updated_entity)

    retrieved = await repo.get_entity_by_id("1")
    assert retrieved is not None
    assert retrieved.name == "Updated Name"
    assert retrieved.price == 20.0


@pytest.mark.asyncio
async def test_repository_update_not_found() -> None:
    """Test updating a non-existent entity raises error."""
    repo = MemoryRepository()
    entity = Entity(id="1", name="Test", price=10.0)

    with pytest.raises(ValueError, match="Entity with id '1' not found"):
        await repo.update(entity)


@pytest.mark.asyncio
async def test_repository_delete() -> None:
    """Test deleting an entity from repository."""
    repo = MemoryRepository()
    entity = Entity(id="1", name="Test Entity", price=10.0)
    await repo.save(entity)

    await repo.delete("1")

    retrieved = await repo.get_entity_by_id("1")
    assert retrieved is None


@pytest.mark.asyncio
async def test_repository_delete_not_found() -> None:
    """Test deleting a non-existent entity raises error."""
    repo = MemoryRepository()

    with pytest.raises(ValueError, match="Entity with id '1' not found"):
        await repo.delete("1")
