import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.error_handlers import entity_not_found_handler
from app.api.error_handlers import entity_validation_error_handler
from app.api.v1.endpoints import entities
from app.core.config import settings
from app.core.container import get_container
from app.core.container import reset_container
from app.core.logging import setup_logging
from app.domain.errors import EntityNotFoundError
from app.domain.errors import EntityValidationError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifespan events."""
    log_level = logging.DEBUG if settings.debug else logging.INFO
    setup_logging(level=log_level)
    container = get_container()
    app.state.container = container
    yield
    reset_container()


app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.description }}",
    lifespan=lifespan,
    debug=settings.debug,
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "{{ cookiecutter.project_name }} API"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


# Include API routes
app.include_router(entities.router, prefix="{{ cookiecutter.api_prefix }}", tags=["entities"])


# Register error handlers
app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
app.add_exception_handler(EntityValidationError, entity_validation_error_handler)
