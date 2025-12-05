"""
Example endpoint file.

To create a new endpoint:
1. Create a new endpoint file (e.g., products.py)
2. Create an APIRouter instance: router = APIRouter()
3. Add your endpoints with @router.get(), @router.post(), etc.
4. Import and include in app/api/router.py
"""

from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import status

from app.api.dependencies import get_product_service
from app.domain.models import Product
from app.domain.errors import ProductValidationError
from app.schemas.product import ProductCreateRequest
from app.schemas.product import ProductsListResponse
from app.schemas.product import ProductSchema
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/products", response_model=ProductsListResponse, status_code=status.HTTP_200_OK)
async def list_products(
    service: ProductService = Depends(get_product_service),
) -> ProductsListResponse:
    """List all products."""
    products = await service.get_products()
    return ProductsListResponse(
        products=[ProductSchema.from_domain(p) for p in products],
        count=len(products),
    )


@router.get("/products/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(
    product_id: str = Path(..., description="Product ID"),
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
