"""
Entity endpoint tests.

To create endpoint tests:
1. Import TestClient from fastapi.testclient
2. Override dependencies using app.dependency_overrides
3. Test all endpoint methods (GET, POST, PUT, DELETE, etc.)
4. Seed test data via HTTP API to avoid async/sync issues
"""

from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.api.dependencies import get_entity_service
from app.api.router import app
from app.repositories.memory_repository import MemoryRepository
from app.services.entity_service import EntityService


@pytest.fixture
def memory_repository() -> MemoryRepository:
    """Create a memory repository for testing."""
    return MemoryRepository()


@pytest.fixture
def entity_service(memory_repository) -> EntityService:
    """Create EntityService with test dependencies."""
    return EntityService(repository=memory_repository)


@pytest.fixture
def client(entity_service):
    """Create test client with overridden dependencies."""
    app.dependency_overrides[get_entity_service] = lambda: entity_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_list_entities_empty(client) -> None:
    """Test listing entities when repository is empty."""
    response = client.get("{{ cookiecutter.api_prefix }}/entities")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 0
    assert data["entities"] == []


def test_list_entities_with_items(client) -> None:
    """Test listing entities with existing items."""

    client.post("{{ cookiecutter.api_prefix }}/entities", json={"name": "Entity 1", "price": 10.0})
    client.post("{{ cookiecutter.api_prefix }}/entities", json={"name": "Entity 2", "price": 20.0})

    response = client.get("{{ cookiecutter.api_prefix }}/entities")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 2
    assert len(data["entities"]) == 2


def test_get_entity_by_id(client) -> None:
    """Test getting an entity by ID."""
    # Create entity via API
    create_response = client.post(
        "{{ cookiecutter.api_prefix }}/entities",
        json={"name": "Test Entity", "price": 15.0}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    entity_id = create_response.json()["id"]

    # Retrieve the entity
    response = client.get(f"{{ cookiecutter.api_prefix }}/entities/{entity_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == entity_id
    assert data["name"] == "Test Entity"
    assert data["price"] == 15.0


def test_get_entity_by_id_not_found(client) -> None:
    """Test getting a non-existent entity returns 404."""
    response = client.get(f"{{ cookiecutter.api_prefix }}/entities/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_create_entity(client) -> None:
    """Test creating a new entity."""
    entity_data = {"name": "New Entity", "price": 25.0}
    response = client.post("{{ cookiecutter.api_prefix }}/entities", json=entity_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Entity"
    assert data["price"] == 25.0
    assert "id" in data


def test_create_entity_validation(client) -> None:
    """Test creating an entity with missing required fields."""
    invalid_data = {}  # Missing required fields
    response = client.post("{{ cookiecutter.api_prefix }}/entities", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    assert "detail" in data


def test_list_entities_with_pagination(client) -> None:
    """Test listing entities with pagination."""
    # Create multiple entities
    for i in range(5):
        client.post("{{ cookiecutter.api_prefix }}/entities", json={"name": f"Entity {i}", "price": float(i * 10)})

    # Test offset
    response = client.get("{{ cookiecutter.api_prefix }}/entities?offset=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["entities"]) == 3
    assert data["count"] == 5

    # Test limit
    response = client.get("{{ cookiecutter.api_prefix }}/entities?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["entities"]) == 2
    assert data["count"] == 5

    # Test offset and limit
    response = client.get("{{ cookiecutter.api_prefix }}/entities?offset=1&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["entities"]) == 2
    assert data["count"] == 5


def test_update_entity(client) -> None:
    """Test updating an entity."""
    # Create entity
    create_response = client.post(
        "{{ cookiecutter.api_prefix }}/entities",
        json={"name": "Original Name", "price": 10.0}
    )
    entity_id = create_response.json()["id"]

    # Update entity
    update_response = client.put(
        f"{{ cookiecutter.api_prefix }}/entities/{entity_id}",
        json={"name": "Updated Name", "price": 20.0}
    )
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["name"] == "Updated Name"
    assert data["price"] == 20.0

    # Verify update
    get_response = client.get(f"{{ cookiecutter.api_prefix }}/entities/{entity_id}")
    assert get_response.json()["name"] == "Updated Name"


def test_update_entity_partial(client) -> None:
    """Test updating an entity with partial data."""
    # Create entity
    create_response = client.post(
        "{{ cookiecutter.api_prefix }}/entities",
        json={"name": "Original Name", "price": 10.0, "in_stock": True}
    )
    entity_id = create_response.json()["id"]

    # Update only name
    update_response = client.put(
        f"{{ cookiecutter.api_prefix }}/entities/{entity_id}",
        json={"name": "Updated Name"}
    )
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["name"] == "Updated Name"
    assert data["price"] == 10.0  # Unchanged
    assert data["in_stock"] is True  # Unchanged


def test_update_entity_not_found(client) -> None:
    """Test updating a non-existent entity returns 404."""
    response = client.put(
        f"{{ cookiecutter.api_prefix }}/entities/{uuid4()}",
        json={"name": "Updated Name"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_entity(client) -> None:
    """Test deleting an entity."""
    # Create entity
    create_response = client.post(
        "{{ cookiecutter.api_prefix }}/entities",
        json={"name": "Test Entity", "price": 10.0}
    )
    entity_id = create_response.json()["id"]

    # Delete entity
    delete_response = client.delete(f"{{ cookiecutter.api_prefix }}/entities/{entity_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Verify deletion
    get_response = client.get(f"{{ cookiecutter.api_prefix }}/entities/{entity_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_entity_not_found(client) -> None:
    """Test deleting a non-existent entity returns 404."""
    response = client.delete(f"{{ cookiecutter.api_prefix }}/entities/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

