"""Tests for main.py"""


def test_main(test_client):
    """Test main.py health server status."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is OK"}
