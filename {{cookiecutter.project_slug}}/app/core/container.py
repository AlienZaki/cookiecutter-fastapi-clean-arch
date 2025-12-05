from app.domain.protocols import Repository
from app.services.product_service import ProductService
{% if cookiecutter.include_memory_repository == "yes" %}
from app.repositories.memory_repository import MemoryRepository
{% endif %}


class Container:
    """
    Container for application dependencies with lifecycle management.

    Uses lazy initialization and factory pattern for better testability
    and resource management.
    """

    def __init__(self) -> None:
        """Initialize container (dependencies created lazily)."""
        self._repository: Repository | None = None
        self._product_service: ProductService | None = None

    @property
    def repository(self) -> Repository:
        """Get repository instance."""
        if self._repository is None:
            self._repository = self._create_repository()
        return self._repository

    @property
    def product_service(self) -> ProductService:
        """Get ProductService instance."""
        if self._product_service is None:
            self._product_service = ProductService(repository=self.repository)
        return self._product_service

    def _create_repository(self) -> Repository:
        """Factory method to create repository based on settings.

        In future, can switch based on settings.repository_type
        (e.g., "memory", "postgres", "mongodb").
        """
{% if cookiecutter.include_memory_repository == "yes" %}
        return MemoryRepository()
{% else %}
        raise NotImplementedError(
            "No repository implementation available. "
        )
{% endif %}

    def reset(self) -> None:
        """Reset container state.

        Clears all dependencies, forcing re-initialization on next access.
        """
        self._repository = None
        self._product_service = None


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
