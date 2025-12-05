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

from app.api.dependencies import get_product_service
from app.domain.errors import ProductValidationError
from app.domain.models import Product
from app.schemas.product import ProductCreateRequest
from app.schemas.product import ProductSchema
from app.schemas.product import ProductUpdateRequest
from app.schemas.product import ProductsListResponse
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/products", response_model=ProductsListResponse, status_code=status.HTTP_200_OK)
async def list_products(
    offset: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int | None = Query(None, ge=1, description="Maximum number of products to return"),
    service: ProductService = Depends(get_product_service),
) -> ProductsListResponse:
    """List all products with optional pagination."""
    products = await service.get_products(offset=offset, limit=limit)
    # Get total count for response (without pagination)
    all_products = await service.get_products()
    return ProductsListResponse(
        products=[ProductSchema.from_domain(p) for p in products],
        count=len(all_products),
    )


@router.get("/products/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(
    product_id: Annotated[str, Path(description="Product ID")],
    service: ProductService = Depends(get_product_service),
) -> ProductSchema:
    """Get a product by ID."""
    product = await service.get_product_by_id(product_id)
    return ProductSchema.from_domain(product)


@router.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    request: ProductCreateRequest,
    service: ProductService = Depends(get_product_service),
) -> ProductSchema:
    """Create a new product."""
    try:
        product = Product(
            id=str(uuid4()),
            name=request.name,
            price=request.price,
            in_stock=request.in_stock,
        )
        created = await service.create_product(product)
        return ProductSchema.from_domain(created)
    except ValueError as e:
        raise ProductValidationError(str(e)) from e


@router.put("/products/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: Annotated[str, Path(description="Product ID")],
    request: Annotated[ProductUpdateRequest, Body()],
    service: ProductService = Depends(get_product_service),
) -> ProductSchema:
    """Update an existing product."""
    # Get existing product
    existing_product = await service.get_product_by_id(product_id)
    
    # Create updated product with new values or keep existing ones
    updated_product = Product(
        id=product_id,
        name=request.name if request.name is not None else existing_product.name,
        price=request.price if request.price is not None else existing_product.price,
        in_stock=request.in_stock if request.in_stock is not None else existing_product.in_stock,
    )
    
    try:
        updated = await service.update_product(updated_product)
        return ProductSchema.from_domain(updated)
    except ValueError as e:
        raise ProductValidationError(str(e)) from e


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: Annotated[str, Path(description="Product ID")],
    service: ProductService = Depends(get_product_service),
) -> None:
    """Delete a product by ID."""
    await service.delete_product(product_id)
