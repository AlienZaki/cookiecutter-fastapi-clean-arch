"""
Example service file.

To create a new service:
1. Create a new service file (e.g., product_service.py)
2. Define your service class with business logic
3. Add the service to app/core/container.py
4. Add dependency function in app/api/dependencies.py
"""

from app.domain.errors import EntityNotFoundError
from app.domain.errors import EntityValidationError
from app.domain.models import Entity
from app.domain.protocols import Repository


class EntityService:
    """Service for managing entities."""

    def __init__(self, repository: Repository) -> None:
        """Initialize service with repository."""
        self.repository = repository

    async def create_entity(self, entity: Entity) -> Entity:
        """Create a new entity."""
        try:
            await self.repository.save(entity)
            return entity
        except ValueError as e:
            raise EntityValidationError(str(e)) from e

    async def get_entity_by_id(self, entity_id: str) -> Entity:
        """Get an entity by ID."""
        entity = await self.repository.get_entity_by_id(entity_id)
        if entity is None:
            raise EntityNotFoundError(entity_id)
        return entity

    async def get_entities(self, offset: int = 0, limit: int | None = None) -> list[Entity]:
        """Get all entities with optional pagination.

        Args:
            offset: Number of entities to skip (for pagination)
            limit: Maximum number of entities to return (None for all)

        Returns:
            List of entities
        """
        return await self.repository.list_all(offset=offset, limit=limit)

    async def update_entity(self, entity: Entity) -> Entity:
        """Update an existing entity."""
        try:
            await self.repository.update(entity)
            return entity
        except ValueError as e:
            raise EntityNotFoundError(str(e)) from e

    async def delete_entity(self, entity_id: str) -> None:
        """Delete an entity by ID."""
        try:
            await self.repository.delete(entity_id)
        except ValueError as e:
            raise EntityNotFoundError(str(e)) from e
