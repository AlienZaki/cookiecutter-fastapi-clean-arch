"""
Example service tests.

To create service tests:
1. Create a new test file in the services/ directory (e.g., test_product_service.py)
2. Import your service and domain models
3. Write tests for your service methods
"""

import pytest

from app.domain.errors import EntityNotFoundError
from app.domain.models import Entity
from app.repositories.memory_repository import MemoryRepository
from app.services.entity_service import EntityService


@pytest.mark.asyncio
async def test_entity_service_create() -> None:
    """Test creating an entity through service."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)
    entity = Entity(id="1", name="Test Entity", price=10.0)
    created = await service.create_entity(entity)
    assert created.id == "1"
    assert created.name == "Test Entity"


@pytest.mark.asyncio
async def test_entity_service_get_entities() -> None:
    """Test getting all entities through service."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)
    entity1 = Entity(id="1", name="Entity 1", price=10.0)
    entity2 = Entity(id="2", name="Entity 2", price=20.0)
    await service.create_entity(entity1)
    await service.create_entity(entity2)
    entities = await service.get_entities()
    assert len(entities) == 2


@pytest.mark.asyncio
async def test_entity_service_get_entity_by_id_not_found() -> None:
    """Test getting an entity by ID when entity does not exist."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)
    with pytest.raises(EntityNotFoundError, match="Entity 'non-existent' not found"):
        await service.get_entity_by_id("non-existent")


@pytest.mark.asyncio
async def test_entity_service_get_entities_with_pagination() -> None:
    """Test getting entities with pagination."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)
    for i in range(5):
        entity = Entity(id=str(i), name=f"Entity {i}", price=float(i * 10))
        await service.create_entity(entity)

    # Test offset
    entities = await service.get_entities(offset=2)
    assert len(entities) == 3

    # Test limit
    entities = await service.get_entities(limit=2)
    assert len(entities) == 2

    # Test offset and limit
    entities = await service.get_entities(offset=1, limit=2)
    assert len(entities) == 2


@pytest.mark.asyncio
async def test_entity_service_update_entity() -> None:
    """Test updating an entity through service."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)
    entity = Entity(id="1", name="Original Name", price=10.0)
    await service.create_entity(entity)

    updated_entity = Entity(id="1", name="Updated Name", price=20.0)
    updated = await service.update_entity(updated_entity)

    assert updated.name == "Updated Name"
    assert updated.price == 20.0

    # Verify it's actually updated in repository
    retrieved = await service.get_entity_by_id("1")
    assert retrieved.name == "Updated Name"


@pytest.mark.asyncio
async def test_entity_service_update_entity_not_found() -> None:
    """Test updating a non-existent entity raises error."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)
    entity = Entity(id="1", name="Test", price=10.0)

    with pytest.raises(EntityNotFoundError):
        await service.update_entity(entity)


@pytest.mark.asyncio
async def test_entity_service_delete_entity() -> None:
    """Test deleting an entity through service."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)
    entity = Entity(id="1", name="Test Entity", price=10.0)
    await service.create_entity(entity)

    await service.delete_entity("1")

    # Verify it's deleted
    with pytest.raises(EntityNotFoundError):
        await service.get_entity_by_id("1")


@pytest.mark.asyncio
async def test_entity_service_delete_entity_not_found() -> None:
    """Test deleting a non-existent entity raises error."""
    repo = MemoryRepository()
    service = EntityService(repository=repo)

    with pytest.raises(EntityNotFoundError):
        await service.delete_entity("non-existent")

