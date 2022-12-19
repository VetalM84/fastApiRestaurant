"""Test cases for methods from utils.py."""
from datetime import timedelta

import pytest

from app.crud.utils import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    tip,
    verify_password,
)
from app.db.models import Waiter


@pytest.mark.parametrize("tip_included,expected_output", [(False, 0.0), (True, 5.0)])
def test_tip(mocker, tip_included, expected_output):
    """Test tip amount."""
    mock_bill = mocker.Mock(tip_percent=5, tip_included=tip_included)
    result = tip(amount=100, bill=mock_bill)
    assert result == expected_output


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


def test_authenticate_user(session, mocker):
    """Test authenticate user."""
    waiter = Waiter(
        id=10,
        username="string",
        password="$12$BQhTQ6/OLAmkG/LU6G2J2.ngFk6EI9hBjFNjeTnpj2eVfQ3DCAtT.",
    )
    mocker.patch(
        "app.crud.utils.get_user_by_username",
        return_value=waiter,
    )
    mocker.patch(
        "app.crud.utils.verify_password",
        return_value=True,
    )
    result = authenticate_user(username="string", password="1111", db=session)
    assert result == waiter

    # verify_password fails
    mocker.patch(
        "app.crud.utils.verify_password",
        return_value=False,
    )
    result = authenticate_user(username="string", password="1111", db=session)
    assert not result


@pytest.mark.parametrize(
    "expires_delta,expected_output",
    [(timedelta(minutes=30), "encoded"), (None, "encoded")],
)
def test_create_access_token(mocker, expires_delta, expected_output):
    """Test create access token."""
    mocker.patch("jose.jwt.encode", return_value="encoded")
    result = create_access_token(data={"sub": "string"}, expires_delta=expires_delta)
    assert result == expected_output
