"""Test client config file."""

import pytest
from app.main import app
from starlette.testclient import TestClient


@pytest.fixture(scope="module")
def test_app():
    """Test client initiation for all tests."""
    client = TestClient(app)
    yield client
