"""Pytest fixtures for unit tests."""

import pytest
from fastapi.testclient import TestClient

from app.api.router import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)
