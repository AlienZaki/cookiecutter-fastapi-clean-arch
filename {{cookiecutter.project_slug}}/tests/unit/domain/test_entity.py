"""
Example domain model tests.

To create domain model tests:
1. Create a new test file in the domain/ directory (e.g., test_product.py)
2. Test validation logic in __post_init__
3. Test domain invariants and business rules
"""

from dataclasses import FrozenInstanceError

import pytest

from app.domain.models import Entity


def test_create_valid_entity() -> None:
    """Test creating a valid entity with all fields."""
    entity = Entity(id="1", name="Test Entity", price=10.0, in_stock=True)
    assert entity.id == "1"
    assert entity.name == "Test Entity"
    assert entity.price == 10.0
    assert entity.in_stock is True


def test_create_entity_with_default_in_stock() -> None:
    """Test creating an entity with default in_stock value."""
    entity = Entity(id="1", name="Test Entity", price=10.0)
    assert entity.in_stock is True


def test_create_entity_with_in_stock_false() -> None:
    """Test creating an entity with in_stock=False."""
    entity = Entity(id="1", name="Test Entity", price=10.0, in_stock=False)
    assert entity.in_stock is False


def test_create_entity_with_zero_price() -> None:
    """Test creating an entity with zero price (valid)."""
    entity = Entity(id="1", name="Free Entity", price=0.0)
    assert entity.price == 0.0


def test_create_entity_with_empty_id_raises_error() -> None:
    """Test that creating an entity with empty id raises ValueError."""
    with pytest.raises(ValueError, match="Entity id cannot be empty"):
        Entity(id="", name="Test Entity", price=10.0)


def test_create_entity_with_whitespace_id_raises_error() -> None:
    """Test that creating an entity with whitespace-only id raises ValueError."""
    with pytest.raises(ValueError, match="Entity id cannot be empty"):
        Entity(id="   ", name="Test Entity", price=10.0)


def test_create_entity_with_empty_name_raises_error() -> None:
    """Test that creating an entity with empty name raises ValueError."""
    with pytest.raises(ValueError, match="Entity name cannot be empty"):
        Entity(id="1", name="", price=10.0)


def test_create_entity_with_whitespace_name_raises_error() -> None:
    """Test that creating an entity with whitespace-only name raises ValueError."""
    with pytest.raises(ValueError, match="Entity name cannot be empty"):
        Entity(id="1", name="   ", price=10.0)


def test_create_entity_with_negative_price_raises_error() -> None:
    """Test that creating an entity with negative price raises ValueError."""
    with pytest.raises(ValueError, match="Entity price cannot be negative"):
        Entity(id="1", name="Test Entity", price=-10.0)


def test_entity_is_immutable() -> None:
    """Test that Entity is immutable (frozen dataclass)."""
    entity = Entity(id="1", name="Test Entity", price=10.0)
    with pytest.raises(FrozenInstanceError):
        entity.name = "New Name"  # type: ignore[arg-type]
