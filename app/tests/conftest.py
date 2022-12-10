"""Test client config file."""

import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():
    """Test client initiation for all tests."""
    client = TestClient(app)
    yield client
