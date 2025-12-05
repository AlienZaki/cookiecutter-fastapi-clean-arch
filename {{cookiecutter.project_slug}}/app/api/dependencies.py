from app.core.container import get_container
from app.domain.protocols import Repository
from app.services.entity_service import EntityService


def get_repository() -> Repository:
    """Get repository instance from container."""
    return get_container().repository


def get_entity_service() -> EntityService:
    """Get EntityService instance from container."""
    return get_container().entity_service
