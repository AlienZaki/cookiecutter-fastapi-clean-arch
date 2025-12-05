"""
Example domain model file.

To create a new domain model:
1. Use dataclasses for pure domain entities (framework-agnostic)
2. Add validation logic in __post_init__ or in services
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Product domain model (immutable domain entity)."""

    id: str
    name: str
    price: float
    in_stock: bool = True

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.id or not self.id.strip():
            raise ValueError("Product id cannot be empty")
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.price < 0:
            raise ValueError("Product price cannot be negative")
