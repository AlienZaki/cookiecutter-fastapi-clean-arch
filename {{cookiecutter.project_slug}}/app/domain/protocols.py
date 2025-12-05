"""
Example protocol file.

To create a new protocol:
1. Import Protocol from typing
2. Define your protocol interface
3. Import it in app/core/container.py and app/api/dependencies.py
"""

from typing import Protocol

from app.domain.models import Entity


class Repository(Protocol):
    """Protocol for entity persistence."""

    async def save(self, entity: Entity) -> None:
        """Save an entity."""
        ...

    async def get_entity_by_id(self, entity_id: str) -> Entity | None:
        """Get an entity by ID."""
        ...

    async def list_all(self, offset: int = 0, limit: int | None = None) -> list[Entity]:
        """Retrieve all entities with optional pagination."""
        ...

    async def update(self, entity: Entity) -> None:
        """Update an existing entity.

        Args:
            entity: Entity with updated data

        Raises:
            ValueError: If entity with given ID doesn't exist
        """
        ...

    async def delete(self, entity_id: str) -> None:
        """Delete an entity by ID.

        Args:
            entity_id: ID of the entity to delete

        Raises:
            ValueError: If entity with given ID doesn't exist
        """
        ...
