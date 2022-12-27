"""Tests for bills.py"""


class TestBill:
    """Class contains tests for bills.py."""

    def test_get_bill(self, test_client):
        """Test get a bill by id with a list of the ordered dishes."""
        response = test_client.get("/bills/4")
        assert response.status_code == 200
