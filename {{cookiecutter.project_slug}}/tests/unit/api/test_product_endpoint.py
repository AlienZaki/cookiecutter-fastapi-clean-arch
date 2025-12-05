"""
Product endpoint tests.

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

from app.api.dependencies import get_product_service
from app.api.router import app
from app.repositories.memory_repository import MemoryRepository
from app.services.product_service import ProductService


@pytest.fixture
def memory_repository() -> MemoryRepository:
    """Create a memory repository for testing."""
    return MemoryRepository()


@pytest.fixture
def product_service(memory_repository) -> ProductService:
    """Create ProductService with test dependencies."""
    return ProductService(repository=memory_repository)


@pytest.fixture
def client(product_service):
    """Create test client with overridden dependencies."""
    app.dependency_overrides[get_product_service] = lambda: product_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_list_products_empty(client) -> None:
    """Test listing products when repository is empty."""
    response = client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 0
    assert data["products"] == []


def test_list_products_with_items(client) -> None:
    """Test listing products with existing items."""

    client.post("/api/v1/products", json={"name": "Product 1", "price": 10.0})
    client.post("/api/v1/products", json={"name": "Product 2", "price": 20.0})

    response = client.get("/api/v1/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 2
    assert len(data["products"]) == 2


def test_get_product_by_id(client) -> None:
    """Test getting a product by ID."""
    # Create product via API
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Test Product", "price": 15.0}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    product_id = create_response.json()["id"]

    # Retrieve the product
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product"
    assert data["price"] == 15.0


def test_get_product_by_id_not_found(client) -> None:
    """Test getting a non-existent product returns 404."""
    response = client.get(f"/api/v1/products/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_create_product(client) -> None:
    """Test creating a new product."""
    product_data = {"name": "New Product", "price": 25.0}
    response = client.post("/api/v1/products", json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Product"
    assert data["price"] == 25.0
    assert "id" in data


def test_create_product_validation(client) -> None:
    """Test creating a product with missing required fields."""
    invalid_data = {}  # Missing required fields
    response = client.post("/api/v1/products", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    assert "detail" in data
