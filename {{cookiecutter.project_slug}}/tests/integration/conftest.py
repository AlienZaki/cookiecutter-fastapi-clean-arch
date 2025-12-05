"""
Example integration test fixtures.

To create integration test fixtures:
1. Add your repository and service fixtures here
2. Use them in your integration tests
"""

import pytest
from app.repositories.memory_repository import MemoryRepository
from app.services.product_service import ProductService


@pytest.fixture
def memory_repository() -> MemoryRepository:
    """Create a memory repository for testing."""
    return MemoryRepository()


@pytest.fixture
def product_service(memory_repository: MemoryRepository) -> ProductService:
    """Create ProductService with test dependencies."""
    return ProductService(repository=memory_repository)
