"""Tests for waiters.py"""

import pytest


@pytest.mark.usefixtures("db_data")
class TestWaiter:
    """Class contains tests for waiters.py."""

    def test_create_waiter(self, test_client):
        """Test create a waiter."""
        data = {
            "username": "username",
            "password": "11111111",
        }
        response = test_client.post("/waiters", json=data)
        assert response.status_code == 201
        assert response.json()["username"] == data["username"]

    def test_get_waiter(self, test_client, access_token):
        """Test Get a waiter by id."""
        test_client.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = test_client.get("/waiters/1")
        assert response.status_code == 200

    def test_get_waiter_401(self, test_client):
        """Test Get a waiter by id with no credentials."""
        response = test_client.get("/waiters/1")
        assert response.status_code == 401

    def test_get_all_waiters(self, test_client):
        """Test get all waiters."""
        response = test_client.get("/waiters")
        assert response.status_code == 200
        assert len(response.json()) == 2
