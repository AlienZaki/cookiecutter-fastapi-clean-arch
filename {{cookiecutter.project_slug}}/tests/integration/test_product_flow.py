"""
Example integration tests.

To create integration tests:
1. Create a new file in the integration/ directory (e.g., test_product_flow.py)
2. Import TestClient and app from app.api.router
3. Write tests for complete API flows
"""

from fastapi.testclient import TestClient

from app.api.router import app

client = TestClient(app)


def test_create_and_list_products() -> None:
    """Test complete flow: create product, then list it."""
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Test Product", "price": 10.0}
    )
    assert create_response.status_code == 201
    created_id = create_response.json()["id"]

    list_response = client.get("/api/v1/products")
    assert list_response.status_code == 200
    data = list_response.json()

    assert data["count"] >= 1
    product_ids = [p["id"] for p in data["products"]]
    assert created_id in product_ids
