"""
Domain-specific exceptions.

This module contains pure domain exceptions with no framework dependencies.
To handle these exceptions in FastAPI,
create and register error handlers in app/api/error_handlers.py
"""

{% if cookiecutter.include_entity_example == "yes" %}
class EntityNotFoundError(Exception):
    """Raised when an entity is not found."""

    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
        super().__init__(f"Entity '{entity_id}' not found")


class EntityValidationError(Exception):
    """Raised when entity validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
{% else %}
# Example: Define your domain exceptions here
# 
# class EntityNotFoundError(Exception):
#     """Raised when an entity is not found."""
# 
#     def __init__(self, entity_id: str) -> None:
#         self.entity_id = entity_id
#         super().__init__(f"Entity '{entity_id}' not found")
# 
# 
# class EntityValidationError(Exception):
#     """Raised when entity validation fails."""
# 
#     def __init__(self, message: str) -> None:
#         super().__init__(message)
{% endif %}
