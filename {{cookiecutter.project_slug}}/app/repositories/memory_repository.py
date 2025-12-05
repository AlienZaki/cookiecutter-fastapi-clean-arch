from app.domain.models import Entity


class MemoryRepository:
    """In-memory repository for storing entities."""

    def __init__(self) -> None:
        """Initialize empty storage."""
        self._items: dict[str, Entity] = {}

    async def save(self, entity: Entity) -> None:
        """Save an entity."""
        if not entity.id:
            raise ValueError("Entity must have an id to be saved")
        self._items[entity.id] = entity

    async def get_entity_by_id(self, entity_id: str) -> Entity | None:
        """Get an entity by ID."""
        return self._items.get(entity_id)

    async def list_all(self, offset: int = 0, limit: int | None = None) -> list[Entity]:
        """Retrieve all saved entities with optional pagination."""
        entities = list(self._items.values())
        if offset > 0:
            entities = entities[offset:]
        if limit is not None:
            entities = entities[:limit]
        return entities

    async def update(self, entity: Entity) -> None:
        """Update an existing entity."""
        if not entity.id:
            raise ValueError("Entity must have an id to be updated")
        if entity.id not in self._items:
            raise ValueError(f"Entity with id '{entity.id}' not found")
        self._items[entity.id] = entity

    async def delete(self, entity_id: str) -> None:
        """Delete an entity by ID."""
        if entity_id not in self._items:
            raise ValueError(f"Entity with id '{entity_id}' not found")
        del self._items[entity_id]

    async def clear(self) -> None:
        """Clear all stored items (useful for testing)."""
        self._items.clear()

    def count(self) -> int:
        """Get the number of stored items."""
        return len(self._items)
