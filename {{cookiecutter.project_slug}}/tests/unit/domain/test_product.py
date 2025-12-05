"""
Example domain model tests.

To create domain model tests:
1. Create a new file in the domain/ directory (e.g., test_product.py)
2. Test validation logic in __post_init__
3. Test domain invariants and business rules
"""

import pytest

from dataclasses import FrozenInstanceError

from app.domain.models import Product


def test_create_valid_product() -> None:
    """Test creating a valid product with all fields."""
    product = Product(id="1", name="Test Product", price=10.0, in_stock=True)
    assert product.id == "1"
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.in_stock is True


def test_create_product_with_default_in_stock() -> None:
    """Test creating a product with default in_stock value."""
    product = Product(id="1", name="Test Product", price=10.0)
    assert product.in_stock is True


def test_create_product_with_in_stock_false() -> None:
    """Test creating a product with in_stock=False."""
    product = Product(id="1", name="Test Product", price=10.0, in_stock=False)
    assert product.in_stock is False


def test_create_product_with_zero_price() -> None:
    """Test creating a product with zero price (valid)."""
    product = Product(id="1", name="Free Product", price=0.0)
    assert product.price == 0.0


def test_create_product_with_empty_id_raises_error() -> None:
    """Test that creating a product with empty id raises ValueError."""
    with pytest.raises(ValueError, match="Product id cannot be empty"):
        Product(id="", name="Test Product", price=10.0)


def test_create_product_with_whitespace_id_raises_error() -> None:
    """Test that creating a product with whitespace-only id raises ValueError."""
    with pytest.raises(ValueError, match="Product id cannot be empty"):
        Product(id="   ", name="Test Product", price=10.0)


def test_create_product_with_empty_name_raises_error() -> None:
    """Test that creating a product with empty name raises ValueError."""
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product(id="1", name="", price=10.0)


def test_create_product_with_whitespace_name_raises_error() -> None:
    """Test that creating a product with whitespace-only name raises ValueError."""
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product(id="1", name="   ", price=10.0)


def test_create_product_with_negative_price_raises_error() -> None:
    """Test that creating a product with negative price raises ValueError."""
    with pytest.raises(ValueError, match="Product price cannot be negative"):
        Product(id="1", name="Test Product", price=-10.0)


def test_product_is_immutable() -> None:
    """Test that Product is immutable (frozen dataclass)."""
    product = Product(id="1", name="Test Product", price=10.0)
    with pytest.raises(FrozenInstanceError):
        setattr(product, "name", "New Name")  # type: ignore[arg-type]

