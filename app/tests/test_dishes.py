"""Tests for dishes.py"""


def test_get_dish(test_app):
    """Test get a dish by id, 404, all dishes."""
    response = test_app.get("/dishes/1")
    assert response.status_code == 200

    response = test_app.get("/dishes/100")
    assert response.status_code == 404

    response = test_app.get("/dishes")
    assert response.status_code == 200


def test_create_dish(test_app):
    """Create a dish."""
    data = {
      "name": "ciwi core",
      "description": "Creativity is intelligence having fun.",
      "image_url": "https://video.szekwanyuen1.net/HouseholdKitchenAppliances",
      "cost": 750.09
    }
    response = test_app.post("/dishes", json=data)
    assert response.status_code == 201
