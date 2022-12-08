"""Tests for main.py"""


def test_main(test_app):
    """Test main.py health server status."""
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is OK"}
