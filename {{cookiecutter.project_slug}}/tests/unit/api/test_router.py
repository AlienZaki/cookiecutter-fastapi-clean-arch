"""API endpoint tests."""

from fastapi.testclient import TestClient

from app.api.router import app


def test_root() -> None:
    """Test root endpoint."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health() -> None:
    """Test health endpoint."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
