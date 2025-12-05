"""
Example integration test fixtures.

To create integration test fixtures:
1. Add your repository and service fixtures here
2. Use them in your integration tests
"""

import pytest
from fastapi.testclient import TestClient

from app.api.router import app
from app.core.container import reset_container
from app.repositories.memory_repository import MemoryRepository
{% if cookiecutter.include_entity_example == "yes" %}
from app.services.entity_service import EntityService
{% endif %}


@pytest.fixture(autouse=True)
def reset_container_before_test() -> None:
    """Reset container before each test to ensure test isolation.
    
    This ensures each test starts with a fresh container and repository,
    preventing test pollution from shared state.
    """
    reset_container()
    yield
    reset_container()


@pytest.fixture
def client() -> TestClient:
    """Create a test client for integration tests."""
    return TestClient(app)


@pytest.fixture
def memory_repository() -> MemoryRepository:
    """Create a memory repository for testing."""
    return MemoryRepository()


{% if cookiecutter.include_entity_example == "yes" %}
@pytest.fixture
def entity_service(memory_repository: MemoryRepository) -> EntityService:
    """Create EntityService with test dependencies."""
    return EntityService(repository=memory_repository)
{% else %}
# Example: Add your service fixtures here
# from app.services.entity_service import EntityService
# 
# @pytest.fixture
# def entity_service(memory_repository: MemoryRepository) -> EntityService:
#     """Create EntityService with test dependencies."""
#     return EntityService(repository=memory_repository)
{% endif %}
