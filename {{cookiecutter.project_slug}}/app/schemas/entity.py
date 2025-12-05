"""
Example schema file.

To create a new schema:
1. Create a new schema file (e.g., product.py)
2. Define your request/response schemas using Pydantic BaseModel
"""

from pydantic import BaseModel

from app.domain.models import Entity


class EntitySchema(BaseModel):
    """API schema for entity data."""

    id: str
    name: str
    price: float
    in_stock: bool = True

    @classmethod
    def from_domain(cls, entity: Entity) -> "EntitySchema":
        """Create schema from domain model."""
        return cls(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            in_stock=entity.in_stock,
        )


class EntityCreateRequest(BaseModel):
    """Request schema for creating an entity."""

    name: str
    price: float
    in_stock: bool = True


class EntityUpdateRequest(BaseModel):
    """Request schema for updating an entity."""

    name: str | None = None
    price: float | None = None
    in_stock: bool | None = None


class EntitiesListResponse(BaseModel):
    """Response schema for entity list."""

    entities: list[EntitySchema]
    count: int

