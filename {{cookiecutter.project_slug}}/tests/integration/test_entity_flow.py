"""
Example integration tests.

To create integration tests:
1. Create a new file in the integration/ directory (e.g., test_product_flow.py)
2. Import TestClient and app from app.api.router
3. Write tests for complete API flows
"""

def test_create_and_list_entities(client) -> None:
    """Test complete flow: create entity, then list it."""
    create_response = client.post(
        "{{ cookiecutter.api_prefix }}/entities",
        json={"name": "Test Entity", "price": 10.0}
    )
    assert create_response.status_code == 201
    created_id = create_response.json()["id"]

    list_response = client.get("{{ cookiecutter.api_prefix }}/entities")
    assert list_response.status_code == 200
    data = list_response.json()

    assert data["count"] >= 1
    entity_ids = [e["id"] for e in data["entities"]]
    assert created_id in entity_ids
