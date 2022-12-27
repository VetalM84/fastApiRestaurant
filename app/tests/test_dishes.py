"""Tests for dishes.py"""


class TestDish:
    """Class contains tests for dishes.py."""

    def test_create_dish(self, test_client):
        """Create a dish."""
        data = {
            "id": 1,
            "name": "ciwi core",
            "description": "Creativity is intelligence having fun.",
            "image_url": "https://video.szekwanyuen1.net/HouseholdKitchenAppliances",
            "cost": 750.09,
        }
        response = test_client.post("/dishes", json=data)
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["name"] == "ciwi core"

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
