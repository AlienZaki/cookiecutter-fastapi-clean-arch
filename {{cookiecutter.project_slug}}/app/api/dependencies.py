from app.core.container import get_container
from app.domain.protocols import Repository
from app.services.product_service import ProductService


def get_repository() -> Repository:
    """Get repository instance from container."""
    return get_container().repository


def get_product_service() -> ProductService:
    """Get ProductService instance from container."""
    return get_container().product_service
