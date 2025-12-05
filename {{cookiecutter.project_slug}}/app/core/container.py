from app.domain.protocols import Repository
from app.repositories.memory_repository import MemoryRepository
from app.services.entity_service import EntityService


class Container:
    """
    Container for application dependencies with lifecycle management.

    Uses lazy initialization and factory pattern for better testability
    and resource management.
    """

    def __init__(self) -> None:
        """Initialize container (dependencies created lazily)."""
        self._repository: Repository | None = None
        self._entity_service: EntityService | None = None

    @property
    def repository(self) -> Repository:
        """Get repository instance."""
        if self._repository is None:
            self._repository = self._create_repository()
        return self._repository

    @property
    def entity_service(self) -> EntityService:
        """Get EntityService instance."""
        if self._entity_service is None:
            self._entity_service = EntityService(repository=self.repository)
        return self._entity_service

    def _create_repository(self) -> Repository:
        """Factory method to create repository based on settings.

        In future, can switch based on settings.repository_type
        (e.g., "memory", "postgres", "mongodb").
        """

        return MemoryRepository()


    def reset(self) -> None:
        """Reset container state.

        Clears all dependencies, forcing re-initialization on next access.
        """
        self._repository = None
        self._entity_service = None


_container: Container | None = None


def get_container() -> Container:
    """Get or create container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container() -> None:
    """Reset global container (for testing)."""
    global _container
    if _container is not None:
        _container.reset()
    _container = None
