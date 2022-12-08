"""Tests for waiters.py"""


def test_get_all_waiters(test_app):
    """Test get all waiters."""
    response = test_app.get("/waiters")
    assert response.status_code == 200


def test_get_waiter(test_app):
    """Test Get a waiter by id."""
    response = test_app.get("/waiters/1")
    assert response.status_code == 200
