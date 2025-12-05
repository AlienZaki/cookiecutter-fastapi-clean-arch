from app.core.container import get_container
from app.domain.protocols import Repository
{% if cookiecutter.include_entity_example == "yes" %}
from app.services.entity_service import EntityService
{% endif %}


def get_repository() -> Repository:
    """Get repository instance from container."""
    return get_container().repository


{% if cookiecutter.include_entity_example == "yes" %}
def get_entity_service() -> EntityService:
    """Get EntityService instance from container."""
    return get_container().entity_service
{% else %}
# Example: Add your service dependency functions here
# from app.services.entity_service import EntityService
# 
# def get_entity_service() -> EntityService:
#     """Get EntityService instance from container."""
#     return get_container().entity_service
{% endif %}
