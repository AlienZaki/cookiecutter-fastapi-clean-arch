"""
Example endpoint file.

To create a new endpoint:
1. Create a new endpoint file (e.g., products.py)
2. Create an APIRouter instance: router = APIRouter()
3. Add your endpoints with @router.get(), @router.post(), etc.
4. Import and include in app/api/router.py
"""

from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from fastapi import status

from app.api.dependencies import get_entity_service
from app.domain.models import Entity
from app.schemas.entity import EntityCreateRequest
from app.schemas.entity import EntitySchema
from app.schemas.entity import EntitiesListResponse
from app.schemas.entity import EntityUpdateRequest
from app.services.entity_service import EntityService

router = APIRouter()


@router.get("/entities", response_model=EntitiesListResponse, status_code=status.HTTP_200_OK)
async def list_entities(
    offset: int = Query(0, ge=0, description="Number of entities to skip"),
    limit: int | None = Query(None, ge=1, description="Maximum number of entities to return"),
    service: EntityService = Depends(get_entity_service),
) -> EntitiesListResponse:
    """List all entities with optional pagination."""
    entities = await service.get_entities(offset=offset, limit=limit)
    # Get total count for response (without pagination)
    all_entities = await service.get_entities()
    return EntitiesListResponse(
        entities=[EntitySchema.from_domain(e) for e in entities],
        count=len(all_entities),
    )


@router.get("/entities/{entity_id}", response_model=EntitySchema, status_code=status.HTTP_200_OK)
async def get_entity(
    entity_id: Annotated[str, Path(description="Entity ID")],
    service: EntityService = Depends(get_entity_service),
) -> EntitySchema:
    """Get an entity by ID."""
    entity = await service.get_entity_by_id(entity_id)
    return EntitySchema.from_domain(entity)


@router.post("/entities", response_model=EntitySchema, status_code=status.HTTP_201_CREATED)
async def create_entity(
    request: EntityCreateRequest,
    service: EntityService = Depends(get_entity_service),
) -> EntitySchema:
    """Create a new entity."""
    entity = Entity(
        id=str(uuid4()),
        name=request.name,
        price=request.price,
        in_stock=request.in_stock,
    )
    created = await service.create_entity(entity)
    return EntitySchema.from_domain(created)


@router.put("/entities/{entity_id}", response_model=EntitySchema, status_code=status.HTTP_200_OK)
async def update_entity(
    entity_id: Annotated[str, Path(description="Entity ID")],
    request: Annotated[EntityUpdateRequest, Body()],
    service: EntityService = Depends(get_entity_service),
) -> EntitySchema:
    """Update an existing entity."""
    existing_entity = await service.get_entity_by_id(entity_id)

    # Create updated entity with new values or keep existing ones
    updated_entity = Entity(
        id=entity_id,
        name=request.name if request.name is not None else existing_entity.name,
        price=request.price if request.price is not None else existing_entity.price,
        in_stock=request.in_stock if request.in_stock is not None else existing_entity.in_stock,
    )

    updated = await service.update_entity(updated_entity)
    return EntitySchema.from_domain(updated)


@router.delete("/entities/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(
    entity_id: Annotated[str, Path(description="Entity ID")],
    service: EntityService = Depends(get_entity_service),
) -> None:
    """Delete an entity by ID."""
    await service.delete_entity(entity_id)
