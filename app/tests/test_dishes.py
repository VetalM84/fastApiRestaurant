"""Tests for dishes.py"""

import pytest


@pytest.mark.usefixtures("db_data")
class TestDish:
    """Class contains tests for dishes.py."""

    def test_create_dish(self, test_client, access_token):
        """Create a dish, create a dish with no credentials."""
        data = {
            "name": "ciwi core",
            "description": "Creativity is intelligence having fun.",
            "image_url": "https://video.szekwanyuen1.net/HouseholdKitchenAppliances",
            "cost": 750.09,
        }
        test_client.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = test_client.post("/dishes", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == "ciwi core"

        # Create a dish without credentials.
        test_client.headers.clear()
        response = test_client.post("/dishes", json=data)
        assert response.status_code == 401

    def test_get_dish(self, test_client):
        """Test get a dish by id, 404"""
        response = test_client.get("/dishes/1")
        assert response.status_code == 200

        response = test_client.get("/dishes/100")
        assert response.status_code == 404

    def test_get_all_dishes(self, test_client):
        """Test get all dishes."""
        response = test_client.get("/dishes")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_delete_dish(self, test_client, access_token):
        """Test get a dish by id, 404, 401"""
        test_client.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = test_client.delete("/dishes/1")
        assert response.status_code == 200

        response = test_client.delete("/dishes/100")
        assert response.status_code == 404

        test_client.headers.clear()
        response = test_client.delete("/dishes/2")
        assert response.status_code == 401
