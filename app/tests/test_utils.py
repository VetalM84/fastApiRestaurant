"""Test cases for methods from utils.py."""

import pytest

from app.crud.utils import get_password_hash, tip, verify_password


def test_tip(mocker):
    """Test tip amount."""
    mock_bill = mocker.Mock(tip_percent=5, tip_included=False)
    result = tip(amount=100, bill=mock_bill)
    assert result == 0.0

    mock_bill = mocker.Mock(tip_percent=5, tip_included=True)
    result = tip(amount=100, bill=mock_bill)
    assert result == 5.0


def test_verify_password(mocker):
    """Test verify password."""
    mocker.patch("app.crud.utils.pwd_context.verify", return_value=True)
    result = verify_password(
        plain_password="1111",
        hashed_password="$2b$12$OvWlVVOnafTbNMwiOkDqSOQHkfCy5vj2xgQdZOz6QHZx6ul6VSVtW",
    )
    assert result


def test_get_password_hash(mocker):
    """Test get password hash."""
    mocker.patch(
        "app.crud.utils.pwd_context.hash",
        return_value="$2b$12$OvWlVVOnafTbNMwiOkDqSOQHkfCy5vj2xgQdZOz6QHZx6ul6VSVtW",
    )
    result = get_password_hash(password="1111")
    assert result == "$2b$12$OvWlVVOnafTbNMwiOkDqSOQHkfCy5vj2xgQdZOz6QHZx6ul6VSVtW"
