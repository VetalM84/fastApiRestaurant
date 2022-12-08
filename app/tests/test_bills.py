"""Tests for bills.py"""


def test_get_bill(test_app):
    """Test get a bill by id with a list of the ordered dishes."""
    response = test_app.get("/bills/4")
    assert response.status_code == 200
